document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal"); // Модальное окно
    const openModalCreateBtn = document.getElementById("open-modal-create"); // Кнопка "Создать фичу"
    const closeModalBtn = document.getElementById("close-modal"); // Кнопка закрытия модального окна
    const form = document.getElementById("create-project-form"); // Форма создания фичи
    const deleteButton = document.getElementById('delete-project-button'); // Кнопка удаления
    const confirmDeletePopup = document.getElementById('confirm-delete-popup'); // Попап подтверждения удаления
    const confirmDeleteButton = document.getElementById('confirm-delete'); // Кнопка подтверждения удаления

    let isEditMode = false; // Флаг редактирования
    let featureId = null; // ID фичи

    // Открытие модального окна для создания новой фичи
    openModalCreateBtn.addEventListener("click", function () {
        isEditMode = false;
        featureId = null;
        form.reset(); // Очищаем форму
        resetSelectFields(); // Сбрасываем select поля
        modal.classList.remove("hidden");
    });

    // Закрытие модального окна
    closeModalBtn.addEventListener("click", function () {
        modal.classList.add("hidden");
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.classList.add("hidden");
        }
    });

    // Скрипт для кастомного множественного выбора
    const selectContainer = document.getElementById('select-container');
    const selectItems = document.getElementById('select-items');
    const selectElement = document.getElementById('project-participants');

    if (selectContainer) {
        selectContainer.addEventListener('click', (event) => {
            selectContainer.classList.toggle('active');
            selectItems.classList.toggle('visible-menu');
            console.log('Клик на контейнер выбора участников');
            event.stopPropagation(); // Останавливаем всплытие, чтобы клик не закрывал меню сразу
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
                // Обновляем текст внутри selectContainer, показывая выбранных участников
                selectContainer.textContent = Array.from(selectElement.options)
                    .filter(option => option.selected)
                    .map(option => option.text)
                    .join(', ') || 'Выберите участников';
            }
            // Останавливаем всплытие клика, чтобы меню не закрывалось
            event.stopPropagation();
        });
    }

    // Закрытие меню при клике вне selectContainer и selectItems
    window.addEventListener('click', (event) => {
        if (!selectContainer.contains(event.target) && !selectItems.contains(event.target) && selectItems.classList.contains('visible-menu')) {
            selectContainer.classList.remove('active');
            selectItems.classList.remove('visible-menu');
        }
    });



      // Функция для обновления текста с выбранными участниками
    function updateSelectedParticipants() {
        const selectedOptions = Array.from(document.querySelectorAll('#project-participants option:checked'));
        const selectContainer = document.getElementById('select-container');

        if (selectedOptions.length > 0) {
            const selectedUsernames = selectedOptions.map(option => option.textContent).join(', ');
            selectContainer.textContent = selectedUsernames; // Обновляем текст на контейнере
        } else {
            selectContainer.textContent = 'Выберите участников'; // Возвращаем текст по умолчанию
        }
    }

    // Основная функция загрузки данных фичи
    function loadFeatureData(featureId) {
        fetch(`/projects/features/edit/${featureId}/`)
            .then(response => response.json())
            .then(data => {
                console.log("Полученные данные фичи:", data); // Отладка: выводим полученные данные

                // Заполнение других полей формы
                const nameInput = document.getElementById("project-name");
                if (nameInput) {
                    nameInput.value = data.name;
                }

                const responsibleSelect = document.getElementById("project-responsible");
                if (responsibleSelect) {
                    responsibleSelect.value = data.responsible;
                }

                const descriptionInput = document.getElementById("project-description");
                if (descriptionInput) {
                    descriptionInput.value = data.description;
                }

                const importanceInput = document.getElementById("project-importance");
                if (importanceInput) {
                    importanceInput.value = data.importance;
                }

                const statusSelect = document.getElementById("project-status");
                if (statusSelect) {
                    statusSelect.value = data.status;
                }

                const projectSelect = document.getElementById("project-project");
                if (projectSelect) {
                    projectSelect.value = data.project;
                }

                // Обновление списка тегов
                const tagsSelect = document.getElementById("project-tags");
                if (tagsSelect) {
                    tagsSelect.value = data.tags;
                }

                // Логика для заполнения участников
                const participantsSelect = document.getElementById('project-participants');
                const participantIds = data.participants; // ID участников из данных

                Array.from(participantsSelect.options).forEach(option => {
                    const optionId = parseInt(option.value);
                    if (participantIds.includes(optionId)) {
                        option.selected = true;
                        console.log(`Участник с ID: ${optionId} отмечен как выбранный.`); // Отладка
                    } else {
                        option.selected = false;
                    }
                });

                // Обновляем отображение выбранных участников
                updateSelectedParticipants();

                const dateCreatedInput = document.getElementById('project-date');
                if (dateCreatedInput) {
                    dateCreatedInput.value = data.date_created ? data.date_created.split('T')[0] : ''; // Проверка на наличие даты
                }

                // Контейнер для отображения выбранных участников
                const participantsContainer = document.getElementById("selected-participants-container");
                if (participantsContainer) {
                    participantsContainer.innerHTML = '';

                    if (Array.isArray(data.selected_participants)) {
                        data.selected_participants.forEach(participant => {
                            const participantDiv = document.createElement('div');
                            participantDiv.classList.add('participant');
                            participantDiv.textContent = participant.username;
                            participantsContainer.appendChild(participantDiv);
                        });
                    } else {
                        console.warn("Выбранные участники не найдены или некорректный формат.");
                    }
                }

                // === Добавляем изменение action URL для режима редактирования ===
                const form = document.getElementById("create-project-form");
                if (form) {
                    form.action = `/projects/features/edit/${featureId}/`;
                }

                // Переключаем режим редактирования
                isEditMode = true;
                modal.classList.remove("hidden");
            })
            .catch(error => {
                console.error("Ошибка при загрузке данных фичи:", error);
            });
    }

    // Открытие модального окна для редактирования
    document.querySelectorAll(".open-modal-btn[data-feature-id]").forEach(button => {
        button.addEventListener("click", function () {
            featureId = this.dataset.featureId;
            loadFeatureData(featureId);
        });
    });

    // Сброс значений в select полях
    function resetSelectFields() {
        const tagsSelect = document.getElementById("project-tags");
        tagsSelect.value = ''; // Сбрасываем выбранный тег

        const participantsSelect = document.getElementById("project-participants");
        participantsSelect.selectedIndex = -1; // Сбрасываем выбранных участников
    }

    function closeModal() {
        const modal = document.getElementById("modal");
        modal.classList.add("hidden");
    }

    // Обработка отправки формы
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log(`Отправка формы: ${form.action}`);

            // Проверка валидности формы
            if (!form.checkValidity()) {
                console.error('Форма невалидна. Пожалуйста, проверьте введенные данные.');
                return;
            }

            const formData = new FormData(form);

            // Обработка полей tags и participants, если они существуют в форме
            const tagsField = form.querySelector("#project-tags");
            const participantsField = form.querySelector("#project-participants");

            if (tagsField) {
                const selectedTags = Array.from(tagsField.selectedOptions).map(option => option.value);
                selectedTags.forEach(tag => {
                    // Добавляем тег в FormData, если его еще нет
                    if (!formData.has('tags')) {
                        formData.append('tags', tag);
                    } else {
                        // Проверяем, что тег еще не был добавлен
                        let existingTags = formData.getAll('tags');
                        if (!existingTags.includes(tag)) {
                            formData.append('tags', tag);
                        }
                    }
                });
            }

            if (participantsField) {
                const selectedParticipants = Array.from(participantsField.selectedOptions).map(option => option.value);
                selectedParticipants.forEach(participant => {
                    // Добавляем участника в FormData, если его еще нет
                    if (!formData.has('participants')) {
                        formData.append('participants', participant);
                    } else {
                        let existingParticipants = formData.getAll('participants');
                        if (!existingParticipants.includes(participant)) {
                            formData.append('participants', participant);
                        }
                    }
                });
            }




            // Логирование данных формы с пометкой, заполнены ли поля
            console.log('Данные формы:');
            Array.from(formData.entries()).forEach(([key, value]) => {
                if (value) {
                    console.log(`${key}: ${value} (Заполнено)`);
                } else {
                    console.log(`${key}: (Пусто)`);
                }
            });

            // Отправка данных на сервер
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
                    // Попробуем получить текст ошибки от сервера для анализа
                    return response.text().then(text => {
                        console.error('Ошибка 400. Ответ от сервера:', text);
                        throw new Error('Сеть ответила с ошибкой: ' + response.status);
                    });
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
                                showError(field, errors); // Отображение ошибок для конкретных полей
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
    });


    // Обработчик для открытия попапа подтверждения удаления
    deleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.remove('hidden'); // Показываем попап подтверждения удаления
    });

    // Обработчик подтверждения удаления проекта
    confirmDeleteButton.addEventListener('click', function () {
        if (featureId) {
            fetch(`/projects/features/delete/${featureId}/`, {
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
});



document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('input[placeholder="Поиск"]');
    const featureContainer = document.getElementById('feature-container').getElementsByTagName('tbody')[0];
    const clearButton = document.getElementById('clear-search'); // Кнопка очистки поиска

    // Функция для отправки запроса
    const searchFeatures = () => {
        const query = searchInput.value.trim();

        if (query.length > 0) {
            fetch(`/projects/features/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    featureContainer.innerHTML = ''; // Очистить предыдущие результаты

                    // Если фичи найдены, добавить их в таблицу
                    if (data.features.length > 0) {
                        data.features.forEach(feature => {
                            const row = document.createElement('tr');
                            row.classList.add('hover:bg-gray-50');
                            row.setAttribute('data-feature-id', feature.id);
                            row.setAttribute('data-status', feature.status);

                            row.innerHTML = `
                                <td class="px-4 py-4 border-b">${feature.id}</td>
                                <td class="px-4 py-4 border-b items-center">
                                    <span class="tag font-medium text-sm">${feature.name}</span><br>
                                </td>
                                <td class="px-4 py-4 border-b text-center">
                                    <div class="inline-flex -space-x-2">
                                        ${feature.participants.map(participant => `
                                            <img src="${participant.avatar || '/static/images/icon-user-project.png'}" alt="${participant.name}" class="inline-block border border-white rounded-full w-6 h-6">
                                        `).join('')}
                                    </div>
                                </td>
                                <td class="px-4 py-4 text-center border-b">${feature.project_name}</td>
                                <td class="px-4 py-4 text-center border-b">${feature.date_created}</td>
                                <td class="px-4 py-4 border-b text-center">${feature.priority}</td>
                                <td class="px-4 py-4 border-b text-center">${feature.status}</td>
                                <td class="px-4 py-4 border-b text-center">
                                    <button class="open-modal-btn text-red-600 hover:text-red-800" data-feature-id="${feature.id}">
                                        <svg width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M15.4525 10.7353L15.448 10.7416L9.02434 17.1658L10.9495 19.0903L17.3786 12.6616L15.4525 10.7353Z" fill="#0C0C0C"></path>
                                            <path d="M5.82559 13.9668L7.75078 15.893L14.1753 9.46878L14.1816 9.46428L12.2546 7.53709L5.82559 13.9668Z" fill="#0C0C0C"></path>
                                            <path d="M4.79594 15.4826L3.04625 20.7313C2.93824 21.0544 3.02285 21.4118 3.26406 21.6521C3.43507 21.824 3.66548 21.9167 3.90039 21.9167C3.9958 21.9167 4.0921 21.9014 4.18481 21.8699L9.43297 20.1201L4.79594 15.4826Z" fill="#0C0C0C"></path>
                                            <path d="M19.9401 4.97531C18.5279 3.5639 16.2292 3.5639 14.817 4.97531L13.5282 6.2643L18.6521 11.3888L19.941 10.0998C21.3532 8.68746 21.3532 6.38762 19.9401 4.97531Z" fill="#0C0C0C"></path>
                                        </svg>
                                    </button>
                                </td>
                            `;
                            featureContainer.appendChild(row);
                        });
                    } else {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td colspan="8" class="px-4 py-4 text-center">Фичи не найдены.</td>`;
                        featureContainer.appendChild(row);
                    }
                })
                .catch(error => console.error('Ошибка при поиске фичей:', error));
        } else {
            featureContainer.innerHTML = ''; // Очистить таблицу, если поиск пустой
            loadAllFeatures(); // Показать все фичи, если нет запроса
        }
    };

    // Функция для загрузки всех фичей (если нет поискового запроса)
    const loadAllFeatures = () => {
        fetch('/projects/features/all/')
            .then(response => response.json())
            .then(data => {
                featureContainer.innerHTML = ''; // Очистить таблицу

                if (data.features.length > 0) {
                    data.features.forEach(feature => {
                        const row = document.createElement('tr');
                        row.classList.add('hover:bg-gray-50');
                        row.setAttribute('data-feature-id', feature.id);
                        row.setAttribute('data-status', feature.status);

                        row.innerHTML = `
                            <td class="px-4 py-4 border-b">${feature.id}</td>
                            <td class="px-4 py-4 border-b items-center">
                                <span class="tag font-medium text-sm">${feature.name}</span><br>
                            </td>
                            <td class="px-4 py-4 border-b text-center">
                                <div class="inline-flex -space-x-2">
                                    ${feature.participants.map(participant => `
                                        <img src="${participant.avatar || '/static/images/icon-user-project.png'}" alt="${participant.name}" class="inline-block border border-white rounded-full w-6 h-6">
                                    `).join('')}
                                </div>
                            </td>
                            <td class="px-4 py-4 text-center border-b">${feature.project_name}</td>
                            <td class="px-4 py-4 text-center border-b">${feature.date_created}</td>
                            <td class="px-4 py-4 border-b text-center">${feature.priority}</td>
                            <td class="px-4 py-4 border-b text-center">${feature.status}</td>
                            <td class="px-4 py-4 border-b text-center">
                                <button class="open-modal-btn text-red-600 hover:text-red-800" data-feature-id="${feature.id}">
                                    <svg width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M15.4525 10.7353L15.448 10.7416L9.02434 17.1658L10.9495 19.0903L17.3786 12.6616L15.4525 10.7353Z" fill="#0C0C0C"></path>
                                        <path d="M5.82559 13.9668L7.75078 15.893L14.1753 9.46878L14.1816 9.46428L12.2546 7.53709L5.82559 13.9668Z" fill="#0C0C0C"></path>
                                        <path d="M4.79594 15.4826L3.04625 20.7313C2.93824 21.0544 3.02285 21.4118 3.26406 21.6521C3.43507 21.824 3.66548 21.9167 3.90039 21.9167C3.9958 21.9167 4.0921 21.9014 4.18481 21.8699L9.43297 20.1201L4.79594 15.4826Z" fill="#0C0C0C"></path>
                                        <path d="M19.9401 4.97531C18.5279 3.5639 16.2292 3.5639 14.817 4.97531L13.5282 6.2643L18.6521 11.3888L19.941 10.0998C21.3532 8.68746 21.3532 6.38762 19.9401 4.97531Z" fill="#0C0C0C"></path>
                                    </svg>
                                </button>
                            </td>
                        `;
                        featureContainer.appendChild(row);
                    });
                }
            })
            .catch(error => console.error('Ошибка при загрузке фичей:', error));
    };

    // Обработчик ввода в поле поиска
    searchInput.addEventListener('input', searchFeatures);

    // Обработчик клика по кнопке очистки
    clearButton.addEventListener('click', () => {
        searchInput.value = ''; // Очищаем поле
        searchFeatures(); // Обновляем таблицу
    });

    // Изначальная загрузка всех фич
    loadAllFeatures();
});




