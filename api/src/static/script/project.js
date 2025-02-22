document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modal = document.getElementById('modal');
    const form = document.getElementById('create-project-form');
    const deleteButton = document.getElementById('delete-project-button');
    const confirmDeletePopup = document.getElementById('confirm-delete-popup');
    const confirmDeleteButton = document.getElementById('confirm-delete');
    const logoPreview = document.getElementById('logo-preview');
    const modalTitle = document.querySelector('.modal-title');
    let submitButton = form.querySelector('button[type="submit"]');
    let currentProjectId = null;
     let ckEditorInstance = null;


    // Открытие модального окна для создания проекта
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/projects/create/');
            modalTitle.textContent = 'Создать проект';
            submitButton.textContent = 'Создать проект';
            form.reset();
            clearErrors();

            // Инициализация Select2
            const participantsSelect = document.getElementById('project-participants');
            if (participantsSelect) {
                $(participantsSelect).select2({
                    placeholder: 'Выберите участников',
                    allowClear: true,
                    width: '100%',
                });
            }

            // Функция для очистки выбора участников
            function clearParticipantsSelect() {
                if (participantsSelect) {
                    $(participantsSelect).val(null).trigger('change'); // Очищаем выбор в Select2
                    updateSelectedParticipants(); // Обновляем текстовое представление
                }
            }

            // Пример вызова при закрытии попапа
            const closeButton = document.getElementById('close-popup-button');
            if (closeButton) {
                closeButton.addEventListener('click', function () {
                    clearParticipantsSelect();
                });
            }

            // Сброс логотипа
            if (logoPreview) {
                logoPreview.src = '';
                logoPreview.classList.add('hidden');
            }

            // Очистка значения оригинального элемента <textarea>
            const descriptionField = document.getElementById('project-description');
            if (descriptionField) {
                descriptionField.value = ''; // Очищаем значение <textarea>
            }

            // Инициализация CKEditor, если он еще не создан
            if (!ckEditorInstance) {
                ClassicEditor
                    .create(descriptionField)
                    .then(editor => {
                        ckEditorInstance = editor;
                    });
            } else {
                // Очистка содержимого CKEditor
                ckEditorInstance.setData('');
            }
        });
    }

    // Закрытие модального окна
    function closeModal() {
        // Уничтожаем экземпляр CKEditor, если он существует
        if (ckEditorInstance) {
            ckEditorInstance.destroy().then(() => {
                ckEditorInstance = null; // Обнуляем переменную после уничтожения
            });
        }

        // Скрываем модальное окно
        if (modal) {
            modal.classList.add('hidden');
        }

        // Сбрасываем форму и очищаем ошибки
        if (form) {
            form.reset(); // Сбрасываем значения полей формы
            clearFormErrors(); // Очищаем ошибки валидации
        }

        // Очищаем предварительный просмотр логотипа
        if (logoPreview) {
            logoPreview.src = ''; // Убираем изображение
            logoPreview.classList.add('hidden'); // Скрываем элемент
        }

        // Очищаем текстовое представление выбранных участников
        const selectContainer = document.getElementById('select-container');
        if (selectContainer) {
            selectContainer.textContent = 'Выберите участников'; // Возвращаем placeholder
        }

        // Очищаем значение оригинального элемента <textarea>
        const descriptionField = document.getElementById('project-description');
        if (descriptionField) {
            descriptionField.value = ''; // Очищаем значение <textarea>
        }

        // Очищаем выбор участников в Select2
        const participantsSelect = document.getElementById('project-participants');
        if (participantsSelect) {
            $(participantsSelect).val(null).trigger('change'); // Очищаем выбор
            updateSelectedParticipants(); // Обновляем текстовое представление
        }

        // Очищаем текущий ID проекта
        currentProjectId = null;
    }


    // Обработчики закрытия модального окна
    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }

    document.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Обработка отправки формы
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            // Очищаем предыдущие ошибки
            clearFormErrors();
            // Проверка валидности формы
            if (!form.checkValidity()) {
                console.error('Форма невалидна. Пожалуйста, проверьте введенные данные.');
                form.reportValidity();
                return;
            }
            // Сохраняем данные из CKEditor в поле description
            if (ckEditorInstance) {
                const descriptionField = document.getElementById('project-description');
                if (descriptionField) {
                    descriptionField.value = ckEditorInstance.getData();
                }
            }
            // Создаем FormData
            const formData = new FormData(form);
            // Обработка даты создания
            const dateCreatedField = document.getElementById('project-date_created');
            if (dateCreatedField) {
                const dateValue = dateCreatedField.value; // Значение из поля <input type="datetime-local">
                const isoDateValue = dateValue.replace('T', ' '); // Убираем временную зону
                console.log('Sending date_created:', isoDateValue); // Отладочное сообщение
                formData.set('date_created', isoDateValue); // Устанавливаем значение в FormData
            }
            // Отправляем запрос
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            let url = form.action;
            if (currentProjectId) {
                url = `/projects/edit/${currentProjectId}/`;
            }
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken ? csrfToken.value : '',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.status === 400) {
                    return response.json().then(data => {
                        throw new Error(JSON.stringify(data.errors));
                    });
                }
                if (response.status === 500) {
                    throw new Error('Произошла внутренняя ошибка сервера');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    closeModal();
                    return fetch('/projects/', {
                        method: 'GET',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'Accept': 'text/html'
                        }
                    });
                } else {
                    throw new Error(data.message || 'Неизвестная ошибка при обработке данных');
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Ошибка при получении данных: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                const tempContainer = document.createElement('div');
                tempContainer.innerHTML = html;
                const newTable = tempContainer.querySelector('#table-style-1');
                const currentTable = document.querySelector('#table-style-1');
                if (!newTable || !currentTable) {
                    throw new Error('Таблица проектов не найдена');
                }
                const newTbody = newTable.querySelector('tbody');
                const currentTbody = currentTable.querySelector('tbody');
                if (!newTbody || !currentTbody) {
                    throw new Error('Содержимое таблицы не найдено');
                }
                currentTbody.innerHTML = newTbody.innerHTML;
                initializeTableEventHandlers();
                // Вместо showNotification, вызываем displayFormErrors
                displayFormErrors({ general: ['Операция выполнена успешно'] });
            })
            .catch(error => {
                console.error('Ошибка:', error);
                try {
                    const errors = JSON.parse(error.message);
                    displayFormErrors(errors); // Используем displayFormErrors для отображения ошибок
                } catch (parseError) {
                    console.error('Ошибка при парсинге ошибок:', parseError);
                    displayFormErrors({ general: ['Произошла ошибка при выполнении операции'] });
                }
            });
        });
    }



     // Функция для очистки ошибок
    function clearFormErrors() {
        const errorElements = document.querySelectorAll('.text-red-500');
        errorElements.forEach(errorElement => errorElement.remove());

        const fields = document.querySelectorAll('[name]');
        fields.forEach(field => field.classList.remove('border-red-500'));
    }

    // Функция вывода ошибок
    function displayFormErrors(errors) {
        for (const [field, messages] of Object.entries(errors)) {
            // Ищем элемент по атрибуту name
            const fieldElement = document.querySelector(`[name="${field}"]`);
            if (fieldElement) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'text-red-500 text-sm mt-1';
                errorDiv.textContent = Array.isArray(messages) ? messages.join(', ') : messages;

                // Проверяем, есть ли уже контейнер для ошибок
                let errorContainer = fieldElement.nextElementSibling;
                if (!errorContainer || !errorContainer.classList.contains('text-red-500')) {
                    fieldElement.parentNode.insertBefore(errorDiv, fieldElement.nextSibling);
                } else {
                    errorContainer.textContent = errorDiv.textContent;
                }

                // Добавляем красную рамку к полю
                fieldElement.classList.add('border-red-500');
            } else {
                console.error(`Field element not found for ${field}`);
            }
        }
    }


    // Редактирование проекта
    function handleEditClick() {
        const projectId = this.getAttribute('data-project-id');
        if (!projectId) {
            console.error('ID проекта не найден');
            return;
        }

        fetch(`/projects/edit/${projectId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 403) {
                    console.error('Ошибка 403: У вас нет прав для редактирования этого проекта');
                    throw new Error('У вас нет прав для редактирования этого проекта');
                }
                console.error(`Ошибка при получении данных проекта: ${response.status}`);
                throw new Error('Ошибка при получении данных проекта');
            }
            return response.json();
        })
        .then(data => {
            currentProjectId = projectId; // Устанавливаем текущий ID проекта
            fillEditForm(data);
            modal.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Ошибка:', error);
            try {
                // Парсим ошибки из JSON-ответа
                const errors = JSON.parse(error.message); // Преобразуем строку ошибок в объект
                // Отображаем ошибки в форме
                displayFormErrors(errors);
            } catch (parseError) {
                console.error('Ошибка при парсинге ошибок:', parseError);
                showNotification('Произошла ошибка при выполнении операции', 'error');
            }
            clearErrors(); // Очищаем предыдущие ошибки перед отображением новых
        });
    }

    // Инициализация обработчиков для кнопок редактирования
    const editProjectButtons = document.querySelectorAll('.edit-project-button');
    editProjectButtons.forEach(button => {
        button.addEventListener('click', handleEditClick);
    });

    // Обработка удаления проекта
    if (deleteButton && confirmDeletePopup) {
        deleteButton.addEventListener('click', function () {
            if (currentProjectId) {
                confirmDeletePopup.classList.remove('hidden');
            }
        });
    }

    const cancelDeleteButton = document.getElementById('cancel-delete');
    if (cancelDeleteButton && confirmDeletePopup) {
        cancelDeleteButton.addEventListener('click', function () {
            confirmDeletePopup.classList.add('hidden');
        });
    }

    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', function () {
            if (!currentProjectId) {
                showNotification('ID проекта не найден', 'error');
                return;
            }

            fetch(`/projects/delete/${currentProjectId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.status === 403) {
                    throw new Error('У вас нет права для удаления этого проекта');
                }
                if (!response.ok) {
                    throw new Error(`Ошибка при удалении проекта: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    confirmDeletePopup.classList.add('hidden');
                    closeModal();
                    // Обновляем таблицу после удаления
                    return fetch('/projects/', {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                } else {
                    throw new Error(data.message || 'Ошибка при удалении проекта');
                }
            })
            .then(response => response.text())
            .then(html => {
                const tempContainer = document.createElement('div');
                tempContainer.innerHTML = html;

                const newTable = tempContainer.querySelector('#table-style-1');
                const currentTable = document.querySelector('#table-style-1');

                if (newTable && currentTable) {
                    const newTbody = newTable.querySelector('tbody');
                    const currentTbody = currentTable.querySelector('tbody');
                    if (newTbody && currentTbody) {
                        currentTbody.innerHTML = newTbody.innerHTML;
                        initializeTableEventHandlers();
                        showNotification('Проект успешно удален', 'success');
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);

                try {
                    // Парсим ошибки из JSON-ответа
                    const errors = JSON.parse(error.message); // Преобразуем строку ошибок в объект

                    // Отображаем ошибки в форме
                    displayFormErrors(errors);
                } catch (parseError) {
                    console.error('Ошибка при парсинге ошибок:', parseError);
                    showNotification('Произошла ошибка при выполнении операции', 'error');
                }

                clearErrors(); // Очищаем предыдущие ошибки перед отображением новых
            });
        });
    }

    // Обработчик для отображения логотипа
    const logoInput = document.getElementById('logo-input');
    if (logoInput) {
        logoInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    logoPreview.src = e.target.result;
                    logoPreview.classList.remove('hidden');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    function fillEditForm(data) {
        // Выводим весь JSON-объект в консоль
        console.log('Data received:', data);

        modalTitle.textContent = 'Редактирование проекта';
        form.setAttribute('action', `/projects/edit/${data.id}/`);

        // Очищаем предыдущие ошибки перед заполнением формы
        clearErrors();

        // Проверяем наличие ошибок в ответе сервера
        if (data.errors) {
            displayFormErrors(data.errors);
            return; // Прерываем выполнение, если есть ошибки
        }

        const fields = ['name', 'status', 'responsible', 'date_created'];
        fields.forEach(field => {
            const element = document.getElementById(`project-${field}`);
            if (element) {
                console.log(`Processing field: ${field}, value:`, data[field]);
                if (field === 'date_created') {
                    const dateValue = data[field] ? new Date(data[field]).toISOString().slice(0, 16) : '';
                    console.log(`Formatted date for ${field}:`, dateValue);
                    element.value = dateValue; // Устанавливаем значение
                } else {
                    element.value = data[field] || '';
                }
            } else {
                console.error(`Element not found for field: ${field}`);
            }
        });

        // Установка значения для CKEditor
        const descriptionField = document.getElementById('project-description');
        if (descriptionField) {
            if (ckEditorInstance) {
                ckEditorInstance.setData(data.description || '');
            } else {
                ClassicEditor
                    .create(descriptionField)
                    .then(editor => {
                        ckEditorInstance = editor;
                        editor.setData(data.description || ''); // Устанавливаем данные после инициализации
                    });
            }
        }

        // Заполнение логотипа
        if (data.logo) {
            logoPreview.src = data.logo;
            logoPreview.classList.remove('hidden');
        } else {
            logoPreview.classList.add('hidden');
        }

        // Заполнение участников
        const participantsSelect = document.getElementById('project-participants');
        if (participantsSelect && data.participants) {
            // Инициализация Select2, если она ещё не выполнена
            if (!$(participantsSelect).hasClass('select2-hidden-accessible')) {
                $(participantsSelect).select2({
                    placeholder: 'Выберите участников',
                    allowClear: true,
                    width: '100%',
                });
            }

            // Получаем массив ID участников из данных
            const participantIds = data.participants.map(participant => participant.id);

            // Устанавливаем selected для соответствующих опций
            Array.from(participantsSelect.options).forEach(option => {
                option.selected = participantIds.includes(parseInt(option.value, 10));
            });

            // Обновляем состояние Select2
            $(participantsSelect).trigger('change');

            // Обновляем текстовое представление
            updateSelectedParticipants();
        }

        submitButton.textContent = 'Сохранить';
    }

    // Функция для обновления текстового представления выбранных участников
    function updateSelectedParticipants() {
        const selectedOptions = Array.from(document.querySelectorAll('#project-participants option:checked'));
        const selectContainer = document.getElementById('select-container');
        if (selectContainer) {
            if (selectedOptions.length > 0) {
                const selectedUsernames = selectedOptions.map(option => option.textContent).join(', ');
                selectContainer.textContent = selectedUsernames;
            } else {
                selectContainer.textContent = 'Выберите участников';
            }
        }
    }

    function clearErrors() {
        const errorDivs = form.querySelectorAll('.text-red-500'); // Ищем все элементы с классом ошибки
        errorDivs.forEach(div => div.remove());
    }



    function initializeTableEventHandlers() {
        const editButtons = document.querySelectorAll('.edit-project-button');
        editButtons.forEach(button => {
            button.addEventListener('click', handleEditClick);
        });

        const deleteButtons = document.querySelectorAll('.delete-project-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                currentProjectId = this.getAttribute('data-project-id');
                if (confirmDeletePopup) {
                    confirmDeletePopup.classList.remove('hidden');
                }
            });
        });

        const sortButtons = document.querySelectorAll('.sort-column');
        sortButtons.forEach(button => {
            button.addEventListener('click', () => {
                const columnIndex = button.getAttribute('data-column-index');
                if (columnIndex) {
                    sortTable(parseInt(columnIndex));
                }
            });
        });
    }



    function clearErrors() {
        const errorDivs = form.querySelectorAll('.error');
        errorDivs.forEach(div => div.remove());
    }


});

// Функция сортировки таблицы
function sortTable(columnIndex) {
    const table = document.getElementById("table-style-1");
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.querySelectorAll("tr"));

    const isAscending = table.dataset.sortOrder === "asc";
    const direction = isAscending ? 1 : -1;

    rows.sort((a, b) => {
        const aText = a.children[columnIndex].textContent.trim();
        const bText = b.children[columnIndex].textContent.trim();

        if (!isNaN(aText) && !isNaN(bText)) {
            return (Number(aText) - Number(bText)) * direction;
        } else {
            return aText.localeCompare(bText) * direction;
        }
    });

    rows.forEach(row => tbody.appendChild(row));
    table.dataset.sortOrder = isAscending ? "desc" : "asc";

    // Update sort arrow styles
    document.querySelectorAll(".sort-arrow").forEach(span => {
        span.textContent = "↕";
    });
    const arrow = table.dataset.sortOrder === "asc" ? "↑" : "↓";
    document.getElementById(`sort-arrow-${columnIndex}`).textContent = arrow;
}