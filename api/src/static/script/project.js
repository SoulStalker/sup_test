document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modal = document.getElementById('modal');
    const form = document.getElementById('create-project-form');
    const deleteButton = document.getElementById('delete-project-button'); // Кнопка удаления
    const confirmDeletePopup = document.getElementById('confirm-delete-popup'); // Попап подтверждения удаления
    const confirmDeleteButton = document.getElementById('confirm-delete'); // Кнопка подтверждения удаления
    const logoPreview = document.getElementById('logo-preview'); // Элемент для показа логотипа

    let submitButton = form.querySelector('button[type="submit"]');
    let currentProjectId = null; // Переменная для хранения текущего ID проекта

    // Открытие модального окна для создания проекта
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/projects/create/');
            submitButton.textContent = 'Создать проект';
            form.reset();
            clearErrors(); // Очистить ошибки при открытии окна

            // Сброс выбора участников
            const participantsSelect = document.getElementById('project-participants');
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

        // Сброс логотипа
        logoPreview.src = '';
        logoPreview.classList.add('hidden'); // Скрытие логотипа

        // Сброс текста выбора участников
        const selectContainer = document.getElementById('select-container');
        selectContainer.textContent = 'Выберите участников';

        // Сброс выбора участников
        const participantsSelect = document.getElementById('project-participants');
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

    // Редактирование проекта
    const editProjectButtons = document.querySelectorAll('.edit-project-button');

    editProjectButtons.forEach(button => {
        button.addEventListener('click', function () {
            currentProjectId = this.getAttribute('data-project-id'); // Получаем ID проекта
            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные проекта через fetch
            fetch(`/projects/edit/${currentProjectId}/`)
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
                    document.getElementById('project-name').value = data.name || '';
                    document.getElementById('project-description').value = data.description || '';
                    document.getElementById('project-status').value = data.status || '';
                    document.getElementById('project-responsible').value = data.responsible || '';

                    // Обновляем логотип проекта
                    if (data.logo) {
                        logoPreview.src = data.logo; // Устанавливаем путь к изображению логотипа
                        logoPreview.classList.remove('hidden'); // Убираем класс hidden для отображения
                    } else {
                        logoPreview.classList.add('hidden'); // Если логотипа нет, скрываем его
                    }

                    // Логика для заполнения участников
                    const participantIds = data.participants.map(participant => participant.id);
                    const participantsSelect = document.getElementById('project-participants');

                    Array.from(participantsSelect.options).forEach(option => {
                        option.selected = participantIds.includes(parseInt(option.value));
                    });

                    // Обновляем отображение выбранных участников
                    updateSelectedParticipants(participantIds);

                    const dateCreatedInput = document.getElementById('project-date');
                    if (dateCreatedInput) {
                        dateCreatedInput.value = data.date_created ? data.date_created.split('T')[0] : ''; // Проверка на наличие даты
                    }

                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/projects/edit/${currentProjectId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"

                    // Проверка логики для передачи логотипа
                    const logoInput = document.getElementById('project-logo');
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

    // Обработчик подтверждения удаления проекта
    confirmDeleteButton.addEventListener('click', function () {
        if (currentProjectId) {
            fetch(`/projects/delete/${currentProjectId}/`, {
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

                    // Перенаправляем на страницу проектов
                    window.location.reload(); // Это обновит текущую страницу
                } else {
                    alert('Ошибка: ' + data.message); // Показываем сообщение об ошибке
                }
            })
            .catch(error => console.error('Ошибка при удалении проекта:', error));
        }
    });

    // Обработчик отмены удаления проекта
    const cancelDeleteButton = document.getElementById('cancel-delete'); // Кнопка отмены удаления
    cancelDeleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.add('hidden'); // Скрываем попап подтверждения удаления
    });

    // Функция для обновления текста с выбранными участниками
    function updateSelectedParticipants(participantIds) {
        const selectedOptions = Array.from(document.querySelectorAll('#project-participants option:checked'));

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

    // Обработчик для отображения логотипа
    const logoInput = document.getElementById('logo-input');
    if (logoInput) {
        logoInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function (e) {
                logoPreview.src = e.target.result; // Отображаем логотип
                logoPreview.classList.remove('hidden'); // Показываем логотип
            };
            if (file) {
                reader.readAsDataURL(file);
            }
        });
    }
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







document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('input[placeholder="Поиск"]'); // Поле для ввода поискового запроса
    const featureContainer = document.getElementById('feature-container').getElementsByTagName('tbody')[0]; // Контейнер для отображения фичей

    // Обработчик события на ввод текста в поле поиска
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();

        // Если строка пустая, не отправляем запрос
        if (!query) {
            return;
        }

        // Отправляем запрос на сервер
        fetch(`/features/search/?q=${encodeURIComponent(query)}`)
            .then(response => {
                // Проверяем, что сервер возвращает статус 200
                if (!response.ok) {
                    throw new Error('Ошибка сервера');
                }
                return response.json();
            })
            .then(data => {
                // Очистка предыдущих результатов
                featureContainer.innerHTML = '';

                // Если фичи найдены, добавляем их в таблицу
                if (data.features && data.features.length > 0) {
                    data.features.forEach(feature => {
                        const row = document.createElement('tr');
                        row.classList.add('hover:bg-gray-50');

                        row.innerHTML = `
                            <td class="px-4 py-4 border-b text-left">${feature.id}</td>
                            <td class="px-4 py-4 border-b text-left truncate">${feature.name}</td>
                            <td class="px-4 py-4 border-b text-left">${feature.description}</td>
                            <td class="px-4 py-4 border-b text-left">${feature.date_created}</td>
                            <td class="px-4 py-4 border-b text-center">
                                <button class="text-red-600 hover:text-red-800 edit-feature-button" data-feature-id="${feature.id}">
                                    <!-- Иконка редактирования -->
                                    <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M12.4525 7.73527L12.448 7.74157L6.02434 14.1658L7.94954 16.0903L14.3786 9.66156L12.4525 7.73527Z" fill="#0C0C0C"/>
                                        <path d="M2.82559 10.9668L4.75078 12.893L11.1753 6.46878L11.1816 6.46428L9.2546 4.53709L2.82559 10.9668Z" fill="#0C0C0C"/>
                                        <path d="M1.79594 12.4826L0.0462492 17.7313C-0.0617561 18.0544 0.0228479 18.4118 0.26406 18.6521C0.435068 18.824 0.66548 18.9167 0.900391 18.9167C0.995796 18.9167 1.0921 18.9014 1.18481 18.8699L6.43297 17.1201L1.79594 12.4826Z" fill="#0C0C0C"/>
                                        <path d="M16.9401 1.97531C15.5279 0.563895 13.2292 0.563895 11.817 1.97531L10.5282 3.2643L15.6521 8.38877L16.941 7.09978C18.3532 5.68746 18.3532 3.38762 16.9401 1.97531Z" fill="#0C0C0C"/>
                                    </svg>
                                </button>
                            </td>
                        `;

                        featureContainer.appendChild(row);
                    });
                } else {
                    // Если фичи не найдены, показываем соответствующее сообщение
                    const row = document.createElement('tr');
                    row.innerHTML = `<td colspan="5" class="px-4 py-4 text-center">Фичи не найдены.</td>`;
                    featureContainer.appendChild(row);
                }
            })
            .catch(error => {
                console.error('Ошибка при поиске фичей:', error);
                // Если произошла ошибка, показываем сообщение
                featureContainer.innerHTML = '<tr><td colspan="5" class="px-4 py-4 text-center">Произошла ошибка при поиске фичей.</td></tr>';
            });
    });

    // Обработчик очистки поиска (если используется кнопка очистки)
    const clearSearchButton = document.getElementById('clear-search');
    if (clearSearchButton) {
        clearSearchButton.addEventListener('click', () => {
            // Отправляем запрос для получения всех фич
            fetch('/features/')
                .then(response => response.json())
                .then(data => {
                    // Очистить поле поиска
                    searchInput.value = '';

                    // Очистить и заново заполнить список
                    featureContainer.innerHTML = '';

                    // Если фичи найдены, добавить их в таблицу
                    if (data.features && data.features.length > 0) {
                        data.features.forEach(feature => {
                            const row = document.createElement('tr');
                            row.classList.add('hover:bg-gray-50');

                            row.innerHTML = `
                                <td class="px-4 py-4 border-b text-left">${feature.id}</td>
                                <td class="px-4 py-4 border-b text-left truncate">${feature.name}</td>
                                <td class="px-4 py-4 border-b text-left">${feature.description}</td>
                                <td class="px-4 py-4 border-b text-left">${feature.date_created}</td>
                                <td class="px-4 py-4 border-b text-center">
                                    <button class="text-red-600 hover:text-red-800 edit-feature-button" data-feature-id="${feature.id}">
                                        <!-- Иконка редактирования -->
                                        <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M12.4525 7.73527L12.448 7.74157L6.02434 14.1658L7.94954 16.0903L14.3786 9.66156L12.4525 7.73527Z" fill="#0C0C0C"/>
                                            <path d="M2.82559 10.9668L4.75078 12.893L11.1753 6.46878L11.1816 6.46428L9.2546 4.53709L2.82559 10.9668Z" fill="#0C0C0C"/>
                                            <path d="M1.79594 12.4826L0.0462492 17.7313C-0.0617561 18.0544 0.0228479 18.4118 0.26406 18.6521C0.435068 18.824 0.66548 18.9167 0.900391 18.9167C0.995796 18.9167 1.0921 18.9014 1.18481 18.8699L6.43297 17.1201L1.79594 12.4826Z" fill="#0C0C0C"/>
                                            <path d="M16.9401 1.97531C15.5279 0.563895 13.2292 0.563895 11.817 1.97531L10.5282 3.2643L15.6521 8.38877L16.941 7.09978C18.3532 5.68746 18.3532 3.38762 16.9401 1.97531Z" fill="#0C0C0C"/>
                                        </svg>
                                    </button>
                                </td>
                            `;

                            featureContainer.appendChild(row);
                        });
                    } else {
                        featureContainer.innerHTML = '<tr><td colspan="5" class="px-4 py-4 text-center">Фичи не найдены.</td></tr>';
                    }
                })
                .catch(error => {
                    console.error('Ошибка при очистке поиска:', error);
                });
        });
    }
});

