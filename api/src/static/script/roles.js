// Создание роли
document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('cancel-role');
    const modal = document.getElementById('modal-create-role');
    const form = document.getElementById('create-role-form');
    const clearErrors = () => {
    form.querySelectorAll('.error-message, .general-error, .network-error').forEach(el => el.remove());
    form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    };
    let submitButton = form.querySelector('button[type="submit"]');

    // Открытие модального окна для создания роли
    if (openModalButton) {
        clearErrors();
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/users/roles/create/');
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

// Редактирование роли
document.addEventListener('DOMContentLoaded', function () {
    const editRoleButtons = document.querySelectorAll('.edit-role-button');
    const modal = document.getElementById('modal-create-role');
    const form = document.getElementById('create-role-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const deleteButtons = document.querySelectorAll('.delete-btn');
    const confirmDeletePopup = document.getElementById('confirm-delete-popup');
    const confirmDeleteButton = document.getElementById('confirm-delete');
    const cancelDeleteButton = document.getElementById('cancel-delete');

    let currentDeleteButton = null; // Текущая кнопка для удаления
    let currentRoleId = null; // Текущий ID роли для удаления

    // Обработка редактирования роли
    editRoleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const roleId = this.getAttribute('data-role-id');
            currentRoleId = roleId;// Устанавливаем текущий ID роли
            confirmDeleteButton.setAttribute('data-role-id', currentRoleId);

            const deleteRoleButton = document.getElementById('delete-role');
            deleteRoleButton.setAttribute('data-role-id', roleId);

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные роли через fetch
            fetch(`/users/roles/edit/${roleId}/`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('name').value = data.name;
                    document.getElementById('color').value = data.color;
                    const colorPicker = document.getElementById('color-picker');
                    colorPicker.value = `#${data.color}`;

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/users/roles/edit/${roleId}/`);
                    form.querySelector('button[type="submit"]').textContent = 'Сохранить';
                })
                .catch(error => console.error('Ошибка при загрузке данных роли:', error));
        });
    });

    // Обработка удаления роли
    deleteButtons.forEach(button => {
    button.addEventListener('click', function () {
        console.log("Кнопка удаления:", this); // Проверяем выбранный элемент
        const roleId = this.getAttribute('data-role-id');
        console.log("Удаление роли с ID:", roleId); // Проверяем значение атрибута

        currentRoleId = roleId; // Устанавливаем текущий ID роли для удаления
        currentDeleteButton = this; // Устанавливаем текущую кнопку для удаления

        if (!roleId) {
            console.error("Ошибка: отсутствует data-role-id у кнопки удаления.");
            return;
        }

        // Открываем popup подтверждения удаления
        confirmDeletePopup.classList.remove('hidden');
    });
});


    // Подтверждение удаления
    confirmDeleteButton.addEventListener('click', function () {
        if (currentRoleId) {
            deleteRole(currentRoleId, currentDeleteButton);
            currentRoleId = null; // Сбрасываем текущий ID роли
            currentDeleteButton = null; // Сбрасываем текущую кнопку
        }
        confirmDeletePopup.classList.add('hidden');
    });

    // Отмена удаления
    cancelDeleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.add('hidden');
        currentRoleId = null; // Сбрасываем текущий ID роли
        currentDeleteButton = null; // Сбрасываем текущую кнопку
    });

    // Функция удаления роли
    function deleteRole(roleId, buttonElement) {
        fetch(`/users/roles/delete/${roleId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (response.ok) {
                console.log("Роль успешно удалена");
                modal.classList.add('hidden');
                location.reload();
            } else {
                throw new Error('Ошибка при удалении роли');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при удалении роли');
        });
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const colorInput = document.getElementById('color');
    const colorPicker = document.getElementById('color-picker');

    // Устанавливаем цвет по умолчанию в текстовое поле
    colorInput.value = colorPicker.value.replace('#', '');

    // Обновление текстового поля при выборе цвета
    colorPicker.addEventListener('input', function() {
        console.log("Выбранный цвет:", this.value);
        colorInput.value = this.value.replace('#', ''); // Убираем #
    });

    // Валидация текстового поля для ввода вручную
    colorInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9A-Fa-f]/g, '').slice(0, 6); // Только hex-символы
    });
});
