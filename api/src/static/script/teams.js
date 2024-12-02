document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modal = document.getElementById('modal');
    const form = document.getElementById('create-team-form');
    const deleteButton = document.getElementById('delete-team-button'); // Кнопка удаления
    const confirmDeletePopup = document.getElementById('confirm-delete-popup'); // Попап подтверждения удаления
    const confirmDeleteButton = document.getElementById('confirm-delete'); // Кнопка подтверждения удаления


    let submitButton = form.querySelector('button[type="submit"]');
    let currentTeamId = null; // Переменная для хранения текущего ID команда

    // Открытие модального окна для создания команды
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/teams/create/');
            submitButton.textContent = 'Создать команду';
            form.reset();
            clearErrors(); // Очистить ошибки при открытии окна

            // Сброс выбора участников
            const participantsSelect = document.getElementById('team-participants');
            Array.from(participantsSelect.options).forEach(option => {
                option.selected = false; // Убираем выделение у всех опций
            });

            // Сброс текста выбора участников
            const selectContainer = document.getElementById('select-container');
            selectContainer.textContent = 'Выберите участников';
        });
    }

    // Закрытие модального окна
    function closeModal() {
        modal.classList.add('hidden');
        form.reset(); // Сбрасываем форму
        clearErrors(); // Очищение ошибок

        // Сброс текста выбора участников
        const selectContainer = document.getElementById('select-container');
        selectContainer.textContent = 'Выберите участников';

        // Сброс выбора участников
        const participantsSelect = document.getElementById('team-participants');
        Array.from(participantsSelect.options).forEach(option => {
            option.selected = false; // Убираем выделение у всех опций
        });
    }

    // Обработчик клика по кнопке закрытия модального окна
    closeModalButton.addEventListener('click', closeModal);
    document.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal(); // Закрываем модальное окно при клике вне него
        }
    });

    // Обработка отправки формы
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('Отправка формы создания команды');

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
                closeModal(); // Закрываем модальное окно при успешном ответе
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

    // Редактирование команды
    const editTeamButtons = document.querySelectorAll('.edit-team-button');

    editTeamButtons.forEach(button => {
        button.addEventListener('click', function () {
            currentTeamId = this.getAttribute('data-team-id'); // Получаем ID команда
            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные команда через fetch
            fetch(`/teams/edit/${currentTeamId}/`)
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errData => {
                            throw new Error(`Ошибка ${response.status}: ${errData.message || 'Неизвестная ошибка'}`);
                        });
                    }
                    return response.json();
                })

                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('team-name').value = data.name || '';

                    // Логика для заполнения участников
                    const participantIds = data.participants.map(participant => participant.id);
                    const participantsSelect = document.getElementById('team-participants');

                    Array.from(participantsSelect.options).forEach(option => {
                        option.selected = participantIds.includes(parseInt(option.value));
                    });

                    // Обновляем отображение выбранных участников
                    updateSelectedParticipants(participantIds);

                    const dateCreatedInput = document.getElementById('team-date');
                    if (dateCreatedInput) {
                        dateCreatedInput.value = data.date_created ? data.date_created.split('T')[0] : ''; // Проверка на наличие даты
                    }

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/teams/edit/${currentTeamId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"

                    // Проверка логики для передачи логотипа
                    const logoInput = document.getElementById('team-logo');
                    const currentLogoSrc = logoPreview.src; // Текущий путь к логотипу

                    if (currentLogoSrc) {
                        if (!logoInput.files.length) {
                            // Если изображения нет в input, используем текущее изображение
                            logoInput.value = currentLogoSrc; // Передаем текущий путь к изображению
                        } else {
                            // Если есть новое изображение, используем его
                            logoInput.value = logoInput.files[0]; // Передаем новое загруженное изображение
                        }
                    } else {
                        // Если логотипа нет, и файл не выбран, то можно оставить обработку по умолчанию
                        logoInput.value = ''; // Или можно обработать это как ошибку, если логотип обязателен
                    }
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });

    // Обработчик для открытия попапа подтверждения удаления
    deleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.remove('hidden'); // Показываем попап подтверждения удаления
    });

    // Обработчик подтверждения удаления команды
    confirmDeleteButton.addEventListener('click', function () {
        if (currentTeamId) {
            fetch(`/teams/delete/${currentTeamId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    confirmDeletePopup.classList.add('hidden'); // Закрываем попап подтверждения удаления
                    closeModal(); // Закрываем модальное окно редактирования

                    // Перенаправляем на страницу командов
                    window.location.reload(); // Это обновит текущую страницу
                } else {
                    alert('Ошибка: ' + data.message); // Показываем сообщение об ошибке
                }
            })
            .catch(error => console.error('Ошибка при удалении команда:', error));
        }
    });

    // Обработчик отмены удаления команды
    const cancelDeleteButton = document.getElementById('cancel-delete'); // Кнопка отмены удаления
    cancelDeleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.add('hidden'); // Скрываем попап подтверждения удаления
    });

    // Функция для обновления текста с выбранными участниками
    function updateSelectedParticipants(participantIds) {
        const selectedOptions = Array.from(document.querySelectorAll('#team-participants option:checked'));

        const selectContainer = document.getElementById('select-container');
        if (selectedOptions.length > 0) {
            const selectedUsernames = selectedOptions.map(option => option.textContent).join(', ');
            selectContainer.textContent = selectedUsernames; // Обновляем текст на контейнере
        } else {
            selectContainer.textContent = 'Выберите участников'; // Возвращаем текст по умолчанию
        }
    }

    // Очищение ошибок формы
    const clearErrors = () => {
        console.log('Очищение ошибок формы');
        const errorDivs = form.querySelectorAll('.error');
        errorDivs.forEach(div => div.remove()); // Удаляем все сообщения об ошибках
    };

    // Функция для отображения ошибок
    const showError = (field, errors) => {
        console.error('Ошибки поля', field.name, errors);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = errors.join(', ');
        field.parentNode.insertBefore(errorDiv, field.nextSibling); // Вставляем ошибку после поля
    };

    // Скрипт для кастомного множественного выбора
    const selectContainer = document.getElementById('select-container');
    const selectItems = document.getElementById('select-items');
    const selectElement = document.getElementById('team-participants');

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
