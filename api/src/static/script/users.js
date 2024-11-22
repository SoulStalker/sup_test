// Создание юзера
document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('cancel-user');
    const modal = document.getElementById('modal-create-user');
    const form = document.getElementById('create-user-form');
    const clearErrors = () => {
    form.querySelectorAll('.error-message, .general-error, .network-error').forEach(el => el.remove());
    form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    };
    let submitButton = form.querySelector('button[type="submit"]');

    // Открытие модального окна для создания мита
    if (openModalButton) {
        clearErrors();
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/users/create/');
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

// Редактирование юзера
document.addEventListener('DOMContentLoaded', function () {
    const edituserButtons = document.querySelectorAll('.edit-user-button');
    const modal = document.getElementById('modal-create-user');
    const form = document.getElementById('create-user-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const deleteButtons = document.querySelectorAll('.delete-btn');
    const confirmDeletePopup = document.getElementById('confirm-delete-popup');
    const confirmDeleteButton = document.getElementById('confirm-delete');
    const cancelDeleteButton = document.getElementById('cancel-delete');

    let currentDeleteButton = null; // Текущая кнопка для удаления
    let currentUserId = null; // Текущий ID роли для удаления
    let submitButton = form.querySelector('button[type="submit"]');

    edituserButtons.forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные мита через fetch
            fetch(`/users/update/${userId}/`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('name').value = data.name;
                    document.getElementById('surname').value = data.surname;
                    document.getElementById('email').value = data.email;
                    document.getElementById('tg_nickname').value = data.tg_nickname;
                    document.getElementById('tg_name').value = data.tg_name;
                    document.getElementById('google_meet_nickname').value = data.google_meet_nickname;
                    document.getElementById('gitlab_nickname').value = data.gitlab_nickname;
                    document.getElementById('github_nickname').value = data.github_nickname;
                    document.getElementById('role').value = data.role_id;

                    // Надо добавить заполнение текущих прав пользователя

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/users/update/${userId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });
});
