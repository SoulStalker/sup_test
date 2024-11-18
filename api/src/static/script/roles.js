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
            form.setAttribute('action', '/roles/create/');
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

    let submitButton = form.querySelector('button[type="submit"]');

    editRoleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const RoleId = this.getAttribute('data-role-id');

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные роли через fetch
            fetch(`/roles/edit/${RoleId}/`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('title').value = data.title;
                    document.getElementById('start_time').value = data.start_time;
                    document.getElementById('category').value = data.category;
                    document.getElementById('responsible').value = data.responsible;

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/roles/edit/${roleId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });
});

// Удаление роли
document.addEventListener('DOMContentLoaded', function() {
            const deleteButtons = document.querySelectorAll('.delete-btn');
            const confirmDeletePopup = document.getElementById('confirm-delete-popup');
            const confirmDeleteButton = document.getElementById('confirm-delete');
            const cancelDeleteButton = document.getElementById('cancel-delete');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            let currentRoleId = null;
            let currentDeleteButton = null;

            deleteButtons.forEach(button => {
                button.addEventListener('click', function() {
                    currentRoleId = this.getAttribute('data-role-id');
                    currentDeleteButton = this;
                    confirmDeletePopup.classList.remove('hidden');
                });
            });

            confirmDeleteButton.addEventListener('click', function() {
                if (currentRoleId) {
                    deleteRole(currentRoleId, currentDeleteButton);
                }
                confirmDeletePopup.classList.add('hidden');
            });

            cancelDeleteButton.addEventListener('click', function() {
                confirmDeletePopup.classList.add('hidden');
                currentRoleId = null;
                currentDeleteButton = null;
            });

            function deleteRole(roleId, buttonElement) {
                fetch(`delete/${roleId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => {
                    if (response.ok) {
                        buttonElement.closest('tr').remove();
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
