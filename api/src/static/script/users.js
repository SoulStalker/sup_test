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

// Редактирование мита
document.addEventListener('DOMContentLoaded', function () {
    const edituserButtons = document.querySelectorAll('.edit-user-button');
    const modal = document.getElementById('modal-create-user');
    const form = document.getElementById('create-user-form');

    let submitButton = form.querySelector('button[type="submit"]');

    edituserButtons.forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные мита через fetch
            fetch(`/users/edit/${userId}/`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('title').value = data.title;
                    document.getElementById('start_time').value = data.start_time;
                    document.getElementById('category').value = data.category;
                    document.getElementById('responsible').value = data.responsible;

                   // Заполняем статусы участников
                    data.participants.forEach(participant => {
                        const participantCheckbox = document.getElementById(`participant_${participant.participant_id}`);
                        const participantStatusInput = document.getElementById(`participant_status_${participant.participant_id}`);
                        const container = document.getElementById(`container_${participant.participant_id}`);

                        if (participantCheckbox) {
                            participantCheckbox.checked = true;  // Отмечаем участника
                        }

                        if (participantStatusInput) {
                            participantStatusInput.value = participant.status;  // Проставляем статус
                        }

                        if (container) {
                            setStatus(participant.participant_id, participant.status);  // Устанавливаем статус
                        }
                    });

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/users/edit/${userId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });
});

// Удаление мита
document.addEventListener('DOMContentLoaded', function() {
            const deleteButtons = document.querySelectorAll('.delete-btn');
            const confirmDeletePopup = document.getElementById('confirm-delete-popup');
            const confirmDeleteButton = document.getElementById('confirm-delete');
            const cancelDeleteButton = document.getElementById('cancel-delete');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            let currentuserId = null;
            let currentDeleteButton = null;

            deleteButtons.forEach(button => {
                button.addEventListener('click', function() {
                    currentuserId = this.getAttribute('data-user-id');
                    currentDeleteButton = this;
                    confirmDeletePopup.classList.remove('hidden');
                });
            });

            confirmDeleteButton.addEventListener('click', function() {
                if (currentuserId) {
                    deleteuser(currentuserId, currentDeleteButton);
                }
                confirmDeletePopup.classList.add('hidden');
            });

            cancelDeleteButton.addEventListener('click', function() {
                confirmDeletePopup.classList.add('hidden');
                currentuserId = null;
                currentDeleteButton = null;
            });

            function deleteuser(userId, buttonElement) {
                fetch(`delete/${userId}/`, {
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
                        throw new Error('Ошибка при удалении встречи');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert('Произошла ошибка при удалении встречи');
                });
            }
        });

// Устанавливает статус участника в мите
function setStatus(userId, status) {
    const container = document.getElementById(`container_${userId}`);
    const statusInput = document.getElementById(`participant_status_${userId}`);
    const participantCheckbox = document.getElementById(`participant_${userId}`);

    // Сброс всех цветов
    container.children[0].classList.remove('bg-blue-500');
    container.children[1].classList.remove('bg-green-500');
    container.children[2].classList.remove('bg-red-500');

    // Установка нового цвета и статуса
    if (status === 'PRESENT') {
        container.children[0].classList.add('bg-blue-500');
    } else if (status === 'WARNED') {
        container.children[1].classList.add('bg-green-500');
    } else if (status === 'ABSENT') {
        container.children[2].classList.add('bg-red-500');
    }

    statusInput.value = status;
    participantCheckbox.checked = true;
}

// Добавление новой категории
document.addEventListener('DOMContentLoaded', function () {
    const openCategoryModalButton = document.getElementById('open-add-category-modal');
    const closeCategoryModalButton = document.getElementById('cancel-add-category');
    const categoryModal = document.getElementById('modal-add-category');
    const categoryForm = document.getElementById('add-category-form');
    const categorySelect = document.getElementById('category');

    // Открытие модального окна для добавления категории
    openCategoryModalButton.addEventListener('click', function (e) {
        e.preventDefault();
        categoryModal.classList.remove('hidden');
    });

    // Закрытие модального окна для добавления категории
    closeCategoryModalButton.addEventListener('click', function () {
        categoryModal.classList.add('hidden');
        categoryForm.reset(); // Сбрасываем форму при закрытии
    });

    // Обработка отправки формы добавления категории
    categoryForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const categoryName = document.getElementById('category-name').value;
        const url = categoryForm.action;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'category_name': categoryName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const option = new Option(data.category_name, data.category_id);
                categorySelect.add(option);
                categorySelect.value = data.category_id;

                categoryModal.classList.add('hidden');
                categoryForm.reset();
            } else {
                alert('Ошибка при добавлении категории: ' + (data.error || 'Неизвестная ошибка'));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке формы');
        });
    });
});



// Обработка поиска
function handleSearch(event) {
    tableConfig.searchTerm = event.target.value.toLowerCase();
    tableConfig.currentPage = 1;
}
