document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modal = document.getElementById('modal');
    const form = document.getElementById('create-project-form');

    if (!form) {
        console.error('Форма создания проекта не найдена');
        return;
    }

    const clearErrors = () => {
        console.log('Очищение ошибок формы');
        const errorMessages = form.querySelectorAll('.error-message, .general-error, .network-error');
        errorMessages.forEach(el => el.remove());
        form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    };

    const showError = (field, messages) => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = messages.join(', ');
        field.parentNode.appendChild(errorDiv);
        field.classList.add('error');
        console.error('Ошибка валидации для поля:', field.name, 'Сообщения:', messages);
    };

    const submitButton = form.querySelector('button[type="submit"]');

    // Открытие модального окна для создания проекта
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/projects/create/');
            submitButton.textContent = 'Создать проект';
            form.reset();
            clearErrors(); // Очистить ошибки при открытии окна
        });
        console.log('Открытие модального окна создания проекта');
    }

    // Закрытие модального окна
    if (closeModalButton) {
        closeModalButton.addEventListener('click', function () {
            modal.classList.add('hidden');
            console.log('Закрытие модального окна');
        });
    }

    // Обработка отправки формы
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('Отправка формы создания проекта');

        // Проверка валидности формы
        if (!form.checkValidity()) {
            console.error('Форма невалидна. Пожалуйста, проверьте введенные данные.');
            return;
        }

        const formData = new FormData(form);
        console.log('Данные формы:', Array.from(formData.entries()));

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            console.log('Ответ от сервера:', response);
            if (!response.ok) {
                throw new Error('Сеть ответила с ошибкой: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('Данные от сервера:', data);
            if (data.status === 'success') {
                modal.classList.add('hidden');
                location.reload(); // Перезагрузка страницы для обновления данных
            } else {
                // Обработка ошибок
                if (data.errors) {
                    console.error('Ошибки валидации:', data.errors);
                    Object.entries(data.errors).forEach(([fieldName, errors]) => {
                        const field = form.querySelector(`[name="${fieldName}"]`);
                        if (field) {
                            showError(field, errors);
                        }
                    });
                } else if (data.message) {
                    console.error('Ошибка сервиса:', data.message);
                    const generalErrorDiv = document.createElement('div');
                    generalErrorDiv.className = 'general-error';
                    generalErrorDiv.textContent = data.message;
                    form.insertBefore(generalErrorDiv, form.firstChild);
                }
            }
        })
        .catch(error => {
            console.error('Ошибка сети:', error);
            const networkErrorDiv = document.createElement('div');
            networkErrorDiv.className = 'network-error';
            networkErrorDiv.textContent = 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.';
            form.insertBefore(networkErrorDiv, form.firstChild);
        });
    });

    // Скрипт для кастомного множественного выбора
    const selectContainer = document.getElementById('select-container');
    const selectItems = document.getElementById('select-items');
    const selectElement = document.getElementById('project-participants');

    if (selectContainer) {
        selectContainer.addEventListener('click', () => {
            selectContainer.classList.toggle('active');
            selectItems.classList.toggle('visible-menu');
            console.log('Клик на контейнер выбора участников');
        });
    }

    if (selectItems) {
        selectItems.addEventListener('click', (event) => {
            if (event.target.tagName === 'DIV') {
                const value = event.target.getAttribute('data-value');
                const option = Array.from(selectElement.options).find(option => option.value === value);
                if (option) {
                    option.selected = !option.selected;
                    event.target.classList.toggle('selected');
                    console.log('Выбор участника:', value);
                }
                selectContainer.textContent = Array.from(selectElement.options)
                    .filter(option => option.selected)
                    .map(option => option.text)
                    .join(', ') || 'Выберите участников';
            }
        });
    }
});



// Редактирование проекта
document.addEventListener('DOMContentLoaded', function () {
    const editProjectButtons = document.querySelectorAll('.edit-project-button');
    const modal = document.getElementById('modal');
    const form = document.getElementById('create-project-form');

    let submitButton = form.querySelector('button[type="submit"]');

    editProjectButtons.forEach(button => {
        button.addEventListener('click', function () {
            const projectId = this.getAttribute('data-project-id');

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные проекта через fetch
            fetch(`/projects/edit/${projectId}/`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('project_name').value = data.name;
                    document.getElementById('project_slug').value = data.slug;
                    document.getElementById('project_description').value = data.description;
                    document.getElementById('project_status').value = data.status;
                    document.getElementById('project_responsible').value = data.responsible;

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/projects/edit/${projectId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });

    // Закрытие попапа при нажатии на кнопку закрытия
    const closeModalButton = document.getElementById('close-modal');
    closeModalButton.addEventListener('click', function () {
        modal.classList.add('hidden');
        form.reset(); // Сбрасываем форму
    });

    // Закрытие попапа при клике вне его содержимого
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.classList.add('hidden');
            form.reset(); // Сбрасываем форму
        }
    });
});


