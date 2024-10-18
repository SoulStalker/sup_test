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
// Глобальные переменные для работы с таблицами
const tableConfig = {
    currentPage: 1,
    rowsPerPage: 16,
    totalPages: 0,
    sortColumn: null,
    sortDirection: 'asc',
    searchTerm: ''
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация элементов управления
    const searchInput = document.querySelector('input[type="text"][placeholder="Поиск"]');
    const rowsPerPageSelect = document.getElementById('rows-per-page');
    const prevButton = document.querySelector('.pagination button:first-child');
    const nextButton = document.querySelector('.pagination button:last-child');

    // Добавление обработчиков событий
    searchInput.addEventListener('input', handleSearch);
    rowsPerPageSelect.addEventListener('change', handleRowsPerPageChange);
    prevButton.addEventListener('click', handlePrevPage);
    nextButton.addEventListener('click', handleNextPage);

    // Добавление обработчиков сортировки для обеих таблиц
    initializeSortingHandlers();

    // Первоначальное обновление таблиц
    updateTables();
});

// Обработка поиска
function handleSearch(event) {
    tableConfig.searchTerm = event.target.value.toLowerCase();
    tableConfig.currentPage = 1;
    updateTables();
}

// Обработка изменения количества строк на странице
function handleRowsPerPageChange(event) {
    tableConfig.rowsPerPage = event.target.value === 'Все'
        ? Number.MAX_SAFE_INTEGER
        : parseInt(event.target.value);
    tableConfig.currentPage = 1;
    updateTables();
}

// Обработка пагинации
function handlePrevPage() {
    if (tableConfig.currentPage > 1) {
        tableConfig.currentPage--;
        updateTables();
    }
}

function handleNextPage() {
    if (tableConfig.currentPage < tableConfig.totalPages) {
        tableConfig.currentPage++;
        updateTables();
    }
}

// Инициализация обработчиков сортировки
function initializeSortingHandlers() {
    const table1Headers = document.querySelectorAll('#table-style-1 thead th');
    const table2Headers = document.querySelectorAll('#table-style-2 thead th');

    // Добавляем обработчики для первой таблицы
    table1Headers.forEach((header, index) => {
        if (index <= 4) { // Только для колонок ID, Имя, Фамилия, Ник Telegram, Имя Telegram
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => handleSort(index, 'table-style-1'));
        }
    });

    // Добавляем обработчики для второй таблицы
    table2Headers.forEach((header, index) => {
        if (index <= 2) { // Только для колонок ID, Название, Дата
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => handleSort(index, 'table-style-2'));
        }
    });
}

// Обработка сортировки
function handleSort(columnIndex, tableId) {
    if (tableConfig.sortColumn === columnIndex) {
        tableConfig.sortDirection = tableConfig.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        tableConfig.sortColumn = columnIndex;
        tableConfig.sortDirection = 'asc';
    }

    const table = document.getElementById(tableId);
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        if (columnIndex === 0) { // Для ID используем числовое сравнение
            return tableConfig.sortDirection === 'asc'
                ? parseInt(aValue) - parseInt(bValue)
                : parseInt(bValue) - parseInt(aValue);
        } else if (tableId === 'table-style-2' && columnIndex === 2) { // Для даты
            const aDate = new Date(aValue.split('.').reverse().join('-'));
            const bDate = new Date(bValue.split('.').reverse().join('-'));
            return tableConfig.sortDirection === 'asc'
                ? aDate - bDate
                : bDate - aDate;
        } else { // Для текстовых значений
            return tableConfig.sortDirection === 'asc'
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }
    });

    // Очищаем и заполняем таблицу отсортированными данными
    rows.forEach(row => tbody.appendChild(row));
    updateTables();

    console.log(`Текущая страница: ${tableConfig.currentPage}`);
    console.log(`Всего страниц: ${tableConfig.totalPages}`);
    console.log(`Начальный индекс: ${startIndex}, Конечный индекс: ${endIndex}`);
}

// Обновление таблиц
function updateTables() {
    const activeTable = document.querySelector('#table-style-1:not(.hidden), #table-style-2:not(.hidden)');
    const rows = Array.from(activeTable.querySelectorAll('tbody tr'));

    // Применяем фильтр поиска
    const filteredRows = rows.filter(row => {
        const text = Array.from(row.cells)
            .slice(0, 5) // Только первые 5 колонок для поиска
            .map(cell => cell.textContent.toLowerCase())
            .join(' ');
        return text.includes(tableConfig.searchTerm);
    });

    // Обновляем общее количество страниц
    tableConfig.totalPages = Math.ceil(filteredRows.length / tableConfig.rowsPerPage);

    // Показываем только строки для текущей страницы
    const startIndex = (tableConfig.currentPage - 1) * tableConfig.rowsPerPage;
    const endIndex = startIndex + tableConfig.rowsPerPage;

    rows.forEach(row => row.classList.add('hidden'));
    filteredRows.slice(startIndex, endIndex).forEach(row => row.classList.remove('hidden'));

    // Обновляем UI пагинации
    updatePaginationUI();
}

// Обновление UI пагинации
function updatePaginationUI() {
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    if (!prevButton || !nextButton || !pageInfo) {
        console.error('Проблема с элементами пагинации');
        return;
    }

    prevButton.disabled = tableConfig.currentPage === 1;
    nextButton.disabled = tableConfig.currentPage === tableConfig.totalPages;

    pageInfo.textContent = `${tableConfig.currentPage} из ${tableConfig.totalPages || 1}`;

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
