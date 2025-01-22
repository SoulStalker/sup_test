// Создание прав
document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('cancel-permission');
    const modal = document.getElementById('modal-create-permission');
    const form = document.getElementById('create-permission-form');
    const clearErrors = () => {
    form.querySelectorAll('.error-message, .general-error, .network-error').forEach(el => el.remove());
    form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    };
    let submitButton = form.querySelector('button[type="submit"]');

    // Открытие модального окна для создания прав
    if (openModalButton) {
        clearErrors();
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/users/permissions/create/');
            submitButton.textContent = 'Создать';
            form.reset();
        });
    }

    // Закрытие модального окна
    if (closeModalButton) {
        closeModalButton.addEventListener('click', function () {
            modal.classList.add('hidden');
        });
    }

    // Обработка отправки формы
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            let formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    modal.classList.add('hidden');
                    location.reload();
                } else {
                    // Обработка ошибок
                    if (data.errors) {
                        // Ошибки валидации формы
                        console.error('Ошибки валидации:', data.errors);
                        // Здесь можно добавить код для отображения ошибок в форме
                        Object.entries(data.errors).forEach(([fieldName, errors]) => {
                            const field = form.querySelector(`[name="${fieldName}"]`);
                            if (field) {
                                // Добавляем класс ошибки к полю
                                field.classList.add('error');
                                // Создаем и показываем сообщение об ошибке
                                const errorDiv = document.createElement('div');
                                errorDiv.className = 'error-message';
                                errorDiv.textContent = errors.join(', ');
                                field.parentNode.appendChild(errorDiv);
                            }
                        });
                    } else if (data.message) {
                        // Ошибка от сервиса
                        console.error('Ошибка сервиса:', data.message);
                        // Можно показать общее сообщение об ошибке
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'general-error';
                        errorDiv.textContent = data.message;
                        form.insertBefore(errorDiv, form.firstChild);
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка сети:', error);
                // Показать общее сообщение об ошибке сети
                const errorDiv = document.createElement('div');
                errorDiv.className = 'network-error';
                errorDiv.textContent = 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.';
                form.insertBefore(errorDiv, form.firstChild);
            });
        });
    }
});

// Редактирование прав
document.addEventListener('DOMContentLoaded', function () {
    const editpermissionButtons = document.querySelectorAll('.edit-permission-button');
    const modal = document.getElementById('modal-create-permission');
    const form = document.getElementById('create-permission-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const deleteButtons = document.querySelectorAll('.delete-btn');
    const confirmDeletePopup = document.getElementById('confirm-delete-popup');
    const confirmDeleteButton = document.getElementById('confirm-delete');
    const cancelDeleteButton = document.getElementById('cancel-delete');

    let currentDeleteButton = null; // Текущая кнопка для удаления
    let currentpermissionId = null; // Текущий ID прав для удаления

    // Обработка редактирования прав
    editpermissionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const permissionId = this.getAttribute('data-permission-id');
            currentpermissionId = permissionId;// Устанавливаем текущий ID прав
            confirmDeleteButton.setAttribute('data-permission-id', currentpermissionId);

            const deletepermissionButton = document.getElementById('delete-permission');
            deletepermissionButton.setAttribute('data-permission-id', permissionId);

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные прав через fetch
            fetch(`/users/permissions/update/${permissionId}/`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('name').value = data.name;
                    document.getElementById('code').value = data.code;
                    document.getElementById('description').value = data.description;
                    document.getElementById('content_type').value = data.content_type;
                    document.getElementById('object').value = data.object?.id ?? "";
                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/users/permissions/update/${permissionId}/`);
                    form.querySelector('button[type="submit"]').textContent = 'Сохранить';
                })
                .catch(error => console.error('Ошибка при загрузке данных прав:', error));
        });
    });

    // Обработка удаления прав
    deleteButtons.forEach(button => {
    button.addEventListener('click', function () {
        console.log("Кнопка удаления:", this); // Проверяем выбранный элемент
        const permissionId = this.getAttribute('data-permission-id');
        console.log("Удаление прав с ID:", permissionId); // Проверяем значение атрибута

        currentpermissionId = permissionId; // Устанавливаем текущий ID прав для удаления
        currentDeleteButton = this; // Устанавливаем текущую кнопку для удаления

        if (!permissionId) {
            console.error("Ошибка: отсутствует data-permission-id у кнопки удаления.");
            return;
        }

        // Открываем popup подтверждения удаления
        confirmDeletePopup.classList.remove('hidden');
    });
});


    // Подтверждение удаления
    confirmDeleteButton.addEventListener('click', function () {
        if (currentpermissionId) {
            deletepermission(currentpermissionId, currentDeleteButton);
            currentpermissionId = null; // Сбрасываем текущий ID прав
            currentDeleteButton = null; // Сбрасываем текущую кнопку
        }
        confirmDeletePopup.classList.add('hidden');
    });

    // Отмена удаления
    cancelDeleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.add('hidden');
        currentpermissionId = null; // Сбрасываем текущий ID прав
        currentDeleteButton = null; // Сбрасываем текущую кнопку
    });

    // Функция удаления прав
    function deletepermission(permissionId, buttonElement) {
        fetch(`/users/permissions/delete/${permissionId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (response.ok) {
                console.log("Права успешно удалены");
                modal.classList.add('hidden');
                location.reload();
            } else {
                throw new Error('Ошибка при удалении прав');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при удалении прав');
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const contentTypeSelect = document.getElementById('content_type');
    const objectSelect = document.getElementById('object');

    if (contentTypeSelect) {
        contentTypeSelect.addEventListener('change', function () {
            const contentTypeId = this.value;
            if (contentTypeId) {
                fetch(`/users/permissions/get_objects/?content_type_id=${contentTypeId}`)
                    .then(response => response.json())
                    .then(data => {
                        // Очищаем список объектов
                        objectSelect.innerHTML = '<option value="">Все</option>';
                        // Заполняем список объектов новыми данными
                        data.forEach(obj => {
                            const option = document.createElement('option');
                            option.value = obj.id;
                            option.textContent = obj.name;
                            objectSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Ошибка при загрузке объектов:', error));
            } else {
                // Если ContentType не выбран, очищаем список объектов
                objectSelect.innerHTML = '<option value="">Все</option>';
            }
        });
    }
});
