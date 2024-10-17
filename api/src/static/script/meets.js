function showTableStyle2() {
    document.getElementById('table-style-1').classList.add('hidden');
    document.getElementById('table-style-2').classList.remove('hidden');
    document.getElementById('style2-button').classList.add('active-button');
    document.getElementById('style1-button').classList.remove('active-button');
    document.getElementById('style2-button').classList.remove('inactive-button');
    document.getElementById('style1-button').classList.add('inactive-button');
    document.querySelector('#style2-button svg').classList.add('fill-[#40454D]');
    document.querySelector('#style1-button svg').classList.add('fill-[#FCFEFF]');
}
// переключение на первую таблицу
document.getElementById('style1-button').addEventListener('click', function() {
    document.getElementById('table-style-1').classList.remove('hidden');
    document.getElementById('table-style-2').classList.add('hidden');
    document.getElementById('style1-button').classList.add('active-button');
    document.getElementById('style2-button').classList.remove('active-button');
    document.getElementById('style1-button').classList.remove('inactive-button');
    document.getElementById('style2-button').classList.add('inactive-button');
    document.querySelector('#style1-button svg').classList.add('fill-[#40454D]');
    document.querySelector('#style2-button svg').classList.add('fill-[#FCFEFF]');
});

// переключение на вторую таблицу
document.getElementById('style2-button').addEventListener('click', function() {
    document.getElementById('table-style-1').classList.add('hidden');
    document.getElementById('table-style-2').classList.remove('hidden');
    document.getElementById('style2-button').classList.add('active-button');
    document.getElementById('style1-button').classList.remove('active-button');
    document.getElementById('style2-button').classList.remove('inactive-button');
    document.getElementById('style1-button').classList.add('inactive-button');
    document.querySelector('#style2-button svg').classList.add('fill-[#40454D]');
    document.querySelector('#style1-button svg').classList.add('fill-[#FCFEFF]');
});

// Фильтрация по категориям
document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('category-select');

    // Слушаем изменения в селекторе категорий
    categorySelect.addEventListener('change', function() {
        const selectedCategory = this.value;
        filterTablesByCategory(selectedCategory);
    });

    function filterTablesByCategory(category) {
        const tables = ['table-style-2'];

        // Проходим по всем таблицам
        tables.forEach(tableId => {
            const table = document.getElementById(tableId);
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const rowCategory = row.getAttribute('data-category');

                // Скрываем или показываем строку в зависимости от выбранной категории
                if (category === 'Категория' || rowCategory === category) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});


document.getElementById('category-select').addEventListener('change', function () {
    const selectedCategory = this.value;
    const allColumns = document.querySelectorAll('#table-style-1 th[data-category], #table-style-1 td[data-category]');

    allColumns.forEach(column => {
        if (selectedCategory === 'Категория' || column.getAttribute('data-category') === selectedCategory) {
            column.style.display = ''; // Показать колонку
        } else {
            column.style.display = 'none'; // Скрыть колонку
        }
    });
});

// Создание мита
document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('cancel-meet');
    const modal = document.getElementById('modal-create-meet');
    const form = document.getElementById('create-meet-form');

    let submitButton = form.querySelector('button[type="submit"]');

    // Открытие модального окна для создания мита
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            form.setAttribute('action', '/meets/create/');
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
                    modal.classList.add('hidden'); // Закрыть модальное окно
                    location.reload(); // Обновить страницу
                } else {
                    console.error('Ошибка при создании Meet:', data.error);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
    }
});

// Редактирование мита
document.addEventListener('DOMContentLoaded', function () {
    const editMeetButtons = document.querySelectorAll('.edit-meet-button');
    const modal = document.getElementById('modal-create-meet');
    const form = document.getElementById('create-meet-form');

    let submitButton = form.querySelector('button[type="submit"]');

    editMeetButtons.forEach(button => {
        button.addEventListener('click', function () {
            const meetId = this.getAttribute('data-meet-id');

            // Открываем модальное окно
            modal.classList.remove('hidden');

            // Загружаем данные мита через fetch
            fetch(`/meets/edit/${meetId}/`)
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
                    // Меняем action формы для отправки на обновление
                    form.setAttribute('action', `/meets/edit/${meetId}/`);
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

            let currentMeetId = null;
            let currentDeleteButton = null;

            deleteButtons.forEach(button => {
                button.addEventListener('click', function() {
                    currentMeetId = this.getAttribute('data-meet-id');
                    currentDeleteButton = this;
                    confirmDeletePopup.classList.remove('hidden');
                });
            });

            confirmDeleteButton.addEventListener('click', function() {
                if (currentMeetId) {
                    deleteMeet(currentMeetId, currentDeleteButton);
                }
                confirmDeletePopup.classList.add('hidden');
            });

            cancelDeleteButton.addEventListener('click', function() {
                confirmDeletePopup.classList.add('hidden');
                currentMeetId = null;
                currentDeleteButton = null;
            });

            function deleteMeet(meetId, buttonElement) {
                fetch(`delete/${meetId}/`, {
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


/// Добавление новой категории
document.addEventListener('DOMContentLoaded', function () {
    const openCategoryModalButton = document.getElementById('open-add-category-modal');
    const closeCategoryModalButton = document.getElementById('cancel-add-category');
    const categoryModal = document.getElementById('modal-add-category');
    const categoryForm = document.getElementById('add-category-form');
    const categorySelect = document.getElementById('category');
    const createMeetForm = document.getElementById('create-meet-form');

    // Открытие модального окна для добавления категории
    openCategoryModalButton.addEventListener('click', function (e) {
        e.preventDefault(); // Предотвращаем отправку формы создания meet
        e.stopPropagation(); // Останавливаем всплытие события
        categoryModal.classList.remove('hidden');
    });

    // Закрытие модального окна для добавления категории
    closeCategoryModalButton.addEventListener('click', function () {
        categoryModal.classList.add('hidden');
        categoryForm.reset(); // Сбрасываем форму при закрытии
    });

    // Обработка отправки формы добавления категории
    addCategoryForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const categoryName = document.getElementById('category-name').value;
    const url = `${addCategoryForm.action}?category_name=${encodeURIComponent(categoryName)}`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const option = new Option(data.category_name, data.category_id);
            categorySelect.add(option);
            categorySelect.value = data.category_id;

            categoryModal.classList.add('hidden');
            addCategoryForm.reset();
        } else {
            alert('Ошибка при добавлении категории: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке формы');
    });
});

    // Предотвращаем всплытие событий с модального окна категории на форму создания meet
    categoryModal.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

// Конфигурация пагинации
const paginationConfig = {
    currentPage: 1,
    rowsPerPage: 100,
    totalPages: 0
};

// Инициализация пагинации при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const rowsPerPageSelect = document.querySelector('select');
    const prevButton = document.querySelector('.pagination button:first-child');
    const nextButton = document.querySelector('.pagination button:last-child');

    // Инициализация пагинации
    initPagination();

    // Обработчик изменения количества строк на странице
    rowsPerPageSelect.addEventListener('change', function() {
        paginationConfig.rowsPerPage = parseInt(this.value);
        paginationConfig.currentPage = 1;
        updateTables();
    });

    // Обработчики кнопок пагинации
    prevButton.addEventListener('click', function() {
        if (paginationConfig.currentPage > 1) {
            paginationConfig.currentPage--;
            updateTables();
        }
    });

    nextButton.addEventListener('click', function() {
        if (paginationConfig.currentPage < paginationConfig.totalPages) {
            paginationConfig.currentPage++;
            updateTables();
        }
    });
});

// Инициализация пагинации
function initPagination() {
    const activeTable = document.querySelector('#table-style-1:not(.hidden), #table-style-2:not(.hidden)');
    const rows = activeTable.querySelectorAll('tbody tr');
    const totalRows = Array.from(rows).filter(row => row.style.display !== 'none').length;

    paginationConfig.totalPages = Math.ceil(totalRows / paginationConfig.rowsPerPage);
    updateTables();
    updatePaginationButtons();
}

// Обновление отображения таблиц
function updateTables() {
    const tables = ['table-style-1', 'table-style-2'];

    tables.forEach(tableId => {
        const table = document.getElementById(tableId);
        if (!table.classList.contains('hidden')) {
            const rows = table.querySelectorAll('tbody tr');
            const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');

            const startIndex = (paginationConfig.currentPage - 1) * paginationConfig.rowsPerPage;
            const endIndex = startIndex + paginationConfig.rowsPerPage;

            visibleRows.forEach((row, index) => {
                if (index >= startIndex && index < endIndex) {
                    row.classList.remove('hidden');
                } else {
                    row.classList.add('hidden');
                }
            });
        }
    });

    updatePaginationButtons();
}

// Обновление состояния кнопок пагинации
function updatePaginationButtons() {
    const prevButton = document.querySelector('.pagination button:first-child');
    const nextButton = document.querySelector('.pagination button:last-child');
    const pageInfo = document.querySelector('.text-green-custom');

    prevButton.disabled = paginationConfig.currentPage === 1;
    nextButton.disabled = paginationConfig.currentPage === paginationConfig.totalPages;

    pageInfo.textContent = `${paginationConfig.currentPage} из ${paginationConfig.totalPages}`;

    // Визуальное отображение состояния кнопок
    [prevButton, nextButton].forEach(button => {
        if (button.disabled) {
            button.classList.add('opacity-50', 'cursor-not-allowed');
            button.classList.remove('hover:bg-green-dark');
        } else {
            button.classList.remove('opacity-50', 'cursor-not-allowed');
            button.classList.add('hover:bg-green-dark');
        }
    });
}

// Обновляем пагинацию при переключении таблиц
document.getElementById('style1-button').addEventListener('click', function() {
    setTimeout(initPagination, 0);
});

document.getElementById('style2-button').addEventListener('click', function() {
    setTimeout(initPagination, 0);
});

// Обновляем пагинацию при фильтрации по категориям
document.getElementById('category-select').addEventListener('change', function() {
    setTimeout(() => {
        paginationConfig.currentPage = 1;
        initPagination();
    }, 0);
});