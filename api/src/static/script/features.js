document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal"); // Модальное окно
    const openModalCreateBtn = document.getElementById("open-modal-create"); // Кнопка "Создать фичу"
    const closeModalBtn = document.getElementById("close-modal"); // Кнопка закрытия модального окна
    const form = document.getElementById("create-project-form"); // Форма создания фичи

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
    // Основная функция загрузки данных фичи
    function loadFeatureData(featureId) {
        fetch(`/projects/features/edit/${featureId}/`)
            .then(response => response.json())
            .then(data => {
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

                // Контейнер для отображения выбранных участников
                const participantsContainer = document.getElementById("selected-participants-container");
                if (participantsContainer) {
                    participantsContainer.innerHTML = '';

                    if (Array.isArray(data.selected_participants) && data.selected_participants.every(p => p.username)) {
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


});
