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
    let currentProjectId = null; // Инициализируем текущий ID проекта


    // Открытие модального окна для создания проекта
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/projects/create/');
            modalTitle.textContent = 'Создать проект';
            submitButton.textContent = 'Создать проект';
            form.reset();
            clearErrors();

            // Сброс выбора участников
            const participantsSelect = document.getElementById('project-participants');
            if (participantsSelect) {
                Array.from(participantsSelect.options).forEach(option => {
                    option.selected = false;
                });
            }

            // Сброс текста выбора участников
            const selectContainer = document.getElementById('select-container');
            if (selectContainer) {
                selectContainer.textContent = 'Выберите участников';
            }

            // Сброс логотипа
            if (logoPreview) {
                logoPreview.src = '';
                logoPreview.classList.add('hidden');
            }
        });
    }

    // Закрытие модального окна
    function closeModal() {
        if (modal) {
            modal.classList.add('hidden');
        }
        if (form) {
            form.reset();
            clearErrors();
        }
        if (logoPreview) {
            logoPreview.src = '';
            logoPreview.classList.add('hidden');
        }
        const selectContainer = document.getElementById('select-container');
        if (selectContainer) {
            selectContainer.textContent = 'Выберите участников';
        }
        const participantsSelect = document.getElementById('project-participants');
        if (participantsSelect) {
            Array.from(participantsSelect.options).forEach(option => {
                option.selected = false;
            });
        }
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

            // Проверка валидности формы
            if (!form.checkValidity()) {
                console.error('Форма невалидна. Пожалуйста, проверьте введенные данные.');
                form.reportValidity();
                return;
            }

            const formData = new FormData(form);
            for (let [key, value] of formData.entries()) {}

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

            let url = form.action;
            if (currentProjectId) {
                url = `/projects/edit/${currentProjectId}/`; // Устанавливаем URL для редактирования
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
                if (response.status === 500) {
                    throw new Error('Произошла внутренняя ошибка сервера');
                }
                return response.json().catch(() => {
                    throw new Error('Ошибка при парсинге ответа сервера');
                });
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
                try {
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
                    showNotification('Операция выполнена успешно', 'success', );
                } catch (error) {
                    console.error('Ошибка при обновлении таблицы:', error);
                    throw new Error('Не удалось обновить таблицу проектов');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                showAccessDeniedError(error.message || 'Произошла ошибка при выполнении операции'); // Отображение ошибки в попапе
                showNotification(error.message || 'Произошла ошибка при выполнении операции', 'error');

                clearErrors();

                const errorDiv = document.createElement('div');
                errorDiv.className = 'error general-error';
                errorDiv.textContent = error.message || 'Произошла ошибка при выполнении операции';
                form.insertBefore(errorDiv, form.firstChild);
            });
        });
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
            console.error('Ошибка при редактировании проекта:', error);
            showAccessDeniedError(error.message); // Отображение ошибки в попапе
            showNotification(error.message, 'error');
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
                showAccessDeniedError(error.message); // Отображение ошибки в попапе
                showNotification(error.message, 'error');
                confirmDeletePopup.classList.add('hidden');
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

    // Вспомогательные функции
    function fillEditForm(data) {
        modalTitle.textContent = 'Редактирование проекта';
        form.setAttribute('action', `/projects/edit/${data.id}/`);

        const fields = ['name', 'description', 'status', 'responsible', 'date'];
        fields.forEach(field => {
            const element = document.getElementById(`project-${field}`);
            if (element) {
                element.value = data[field] || '';
            }
        });

        const participantsSelect = document.getElementById('project-participants');
        if (participantsSelect && data.participant_ids) {
            Array.from(participantsSelect.options).forEach(option => {
                option.selected = data.participant_ids.includes(parseInt(option.value));
            });
            updateSelectedParticipants();
        }

        if (data.logo) {
            logoPreview.src = data.logo;
            logoPreview.classList.remove('hidden');
        } else {
            logoPreview.classList.add('hidden');
        }

        submitButton.textContent = 'Сохранить';
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
        const errorDivs = form.querySelectorAll('.error');
        errorDivs.forEach(div => div.remove());
    }
    // Функция для отображения уведомлений в указанном контейнере
    function showNotification(message, type = 'info', containerId = 'access-denied-message') {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер с ID ${containerId} не найден.`);
            return;
        }

        // Создание элемента уведомления
        const notification = document.createElement('div');
        notification.className = `notification ${type === 'error' ? 'text-red-500' : 'text-green-500'} modal-title text-xl text-center font-semibold`;
        notification.textContent = message;

        // Добавление уведомления в контейнер
        container.appendChild(notification);

        // Удаление уведомления через 3 секунды
        setTimeout(() => {
            notification.remove();
        }, 3000);

        // Открываем попап в любом случае
        const popup = document.getElementById('access-denied-popup');
        if (popup) {
            popup.classList.remove('hidden'); // Убираем класс hidden, чтобы показать попап

            // Автоматическое закрытие попапа через 3 секунды
            setTimeout(() => {
                popup.classList.add('hidden'); // Добавляем класс hidden, чтобы скрыть попап
            }, 3000);
        } else {
            console.error('Попап с ID "access-denied-popup" не найден.');
        }
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