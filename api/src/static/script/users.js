$(document).ready(function() {
    $('#permissions').select2({
        width: 'resolve',
        placeholder: 'Выберите права'
    }).on('change', updateSelectedPermissions);
});

function updateSelectedPermissions() {
    const selectedOptions = $('#permissions').select2('data');
    const permissionsContainer = document.getElementById('permissions-container');
    if (permissionsContainer) {
        if (selectedOptions.length > 0) {
            const selectedPermissions = selectedOptions.map(option => option.text).join(', ');
            permissionsContainer.textContent = selectedPermissions;
        } else {
            permissionsContainer.textContent = 'Выберите права';
        }
    }
}

// Функция для очистки формы
function resetFormForCreation(form) {
    form.reset();
    // Очищаем аватар
    const avatarContainer = document.querySelector('.mb-4');
    const avatarImg = avatarContainer.querySelector('img');
    const avatarSpan = avatarContainer.querySelector('span');
    if (avatarImg) avatarImg.style.display = 'none';
    if (avatarSpan) avatarSpan.style.display = 'block';

    // Очищаем мультиселект с правами
    const permissionsSelect = document.getElementById('permissions');
    Array.from(permissionsSelect.options).forEach(option => {
        option.selected = false;
    });
    $('#permissions').trigger('change'); // Обновляем Select2
    updateSelectedPermissions(); // Обновляем текстовое представление выбранных прав

    // Устанавливаем action формы для создания
    form.setAttribute('action', '/users/create/');
}


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

    // Открытие модального окна для создания юзера
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
        // Загружаем данные пользователя через fetch
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
                document.getElementById('team').value = data.team_id;
                document.getElementById('is_active').checked = data.is_active;
                document.getElementById('is_admin').checked = data.is_admin;

                // Обновление аватара
                const avatarContainer = document.querySelector('.mb-4');
                const avatarImg = avatarContainer.querySelector('img');
                const avatarSpan = avatarContainer.querySelector('span');

                if (data.avatar) {
                    if (avatarImg) {
                        avatarImg.src = data.avatar;
                        avatarImg.style.display = 'block';
                    } else {
                        const img = document.createElement('img');
                        img.src = data.avatar;
                        img.alt = 'Аватар';
                        img.style.width = '100px';
                        img.style.height = '100px';
                        avatarContainer.insertBefore(img, avatarContainer.querySelector('.border-dashed'));
                    }
                    if (avatarSpan) avatarSpan.style.display = 'none';
                } else {
                    if (avatarImg) avatarImg.style.display = 'none';
                    if (avatarSpan) avatarSpan.style.display = 'block';
                }

                // Заполняем мультиселект с правами
                const permissionsSelect = document.getElementById('permissions');
                Array.from(permissionsSelect.options).forEach(option => {
                    option.selected = data.permissions_ids.includes(parseInt(option.value, 10));
                });

                // Обновляем состояние Select2 и вызываем функцию для обновления отображения выбранных прав
                $('#permissions').trigger('change'); // Обновляем Select2
                updateSelectedPermissions(); // Обновляем текстовое представление выбранных прав


                // Меняем action формы для отправки на обновление
                form.setAttribute('action', `/users/update/${userId}/`);
                submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
            })
            .catch(error => console.error('Ошибка:', error));
    });
});

});
document.addEventListener('DOMContentLoaded', function () {
    const rowsPerPageSelect = document.getElementById('rows-per-page');
    const rowsPerPageForm = document.getElementById('rows-per-page-form');

    rowsPerPageSelect.addEventListener('change', function () {
        // Сбрасываем номер страницы на 1 при изменении количества элементов
        const pageInput = rowsPerPageForm.querySelector('input[name="page"]');
        if (pageInput) {
            pageInput.value = '1';
        }
        rowsPerPageForm.submit();
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('role-select');
    const teamSelect = document.getElementById('team-select');

    roleSelect.addEventListener('change', filterTables);
    teamSelect.addEventListener('change', filterTables);

    function filterTables() {
        const selectedRole = roleSelect.value;
        const selectedTeam = teamSelect.value;
        const table = document.getElementById('table-container');
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const rowRole = row.getAttribute('data-role');
            const rowTeam = row.getAttribute('data-team');

            const roleMatch = (selectedRole === 'Роль' || rowRole === selectedRole);
            const teamMatch = (selectedTeam === 'Команда' || rowTeam === selectedTeam);

            row.style.display = (roleMatch && teamMatch) ? '' : 'none';
        });
    }
});


// Загрузка аватара
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('avatar');
    const dropzone = fileInput.parentElement;

    // Открыть выбор файла при клике на область
    dropzone.addEventListener('click', function() {
        fileInput.click(); // Имитация клика на input
    });

    // Обновление отображения после выбора файла
    fileInput.addEventListener('change', function() {
        const fileName = fileInput.files[0]?.name || 'Файл не выбран';
        dropzone.querySelector('span').textContent = fileName;
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const sendEmailButton = document.getElementById('submit-user-email');
    const sendEmailInput = document.getElementById('send_email');
    const submitButton = document.getElementById('submit-user');

    // Обработка нажатия кнопки "Создать и отправить Email"
    if (sendEmailButton) {
        sendEmailButton.addEventListener('click', function () {
            sendEmailInput.value = "true"; // Устанавливаем значение true для отправки email
        });
    }

    // Обработка нажатия кнопки "Создать"
    if (submitButton) {
        submitButton.addEventListener('click', function () {
            // Не сбрасываем значение send_email, если кнопка "Создать и отправить Email" не была нажата
            if (sendEmailInput.value !== "true") {
                sendEmailInput.value = "false"; // Сбрасываем значение на false только если кнопка "Создать и отправить Email" не была нажата
            }
        });
    }
});
