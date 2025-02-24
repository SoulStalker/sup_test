document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input'); // Получаем поле поиска
    const tableBody = document.querySelector('table tbody'); // Получаем тело таблицы
    const table = document.getElementById('table-style-1'); // Получаем таблицу

    // Создаем элемент для сообщения "Данных нет"
    const createNoDataMessage = (colSpan) => {
        const noDataMessage = document.createElement('tr');
        const noDataCell = document.createElement('td');
        noDataCell.colSpan = colSpan;
        noDataCell.textContent = 'Данных нет';
        noDataCell.classList.add('text-center', 'text-gray-500', 'py-4');
        noDataMessage.appendChild(noDataCell);
        return noDataMessage;
    };

    const colSpan = table.querySelectorAll('thead th').length;
    let noDataMessage = createNoDataMessage(colSpan);
    tableBody.appendChild(noDataMessage);
    noDataMessage.style.display = 'none'; // Изначально скрываем сообщение

    // Функция для сброса подсветки
    const resetHighlight = () => {
        const highlightedElements = document.querySelectorAll('mark.highlight');
        highlightedElements.forEach(el => {
            el.outerHTML = el.textContent; // Убираем тег <mark>
        });
    };

    // Функция для подсветки найденного текста
    const highlightText = (element, searchText) => {
        const innerText = element.textContent;
        const regex = new RegExp(`(${searchText})`, 'gi'); // Искать слово без учета регистра
        element.innerHTML = innerText.replace(regex, '<mark class="highlight">$1</mark>');
    };

    // Обработчик ввода в поле поиска
    searchInput.addEventListener('input', function () {
        const query = searchInput.value.toLowerCase().trim(); // Получаем строку поиска
        const rows = tableBody.querySelectorAll('tr:not(:last-child)'); // Получаем все строки таблицы, кроме сообщения "Данных нет"
        let hasVisibleRows = false; // Отслеживаем, есть ли видимые строки

        resetHighlight(); // Сбрасываем подсветку перед новым поиском

        rows.forEach(function (row) {
            const cells = row.querySelectorAll('td');
            let match = false;

            // Проверяем, есть ли совпадения в данных таблицы
            cells.forEach(function (cell) {
                if (cell.textContent.toLowerCase().includes(query)) {
                    match = true;
                    highlightText(cell, query); // Подсвечиваем найденное слово
                }
            });

            // Если совпадение есть, показываем строку, иначе скрываем
            if (match) {
                row.style.display = '';
                hasVisibleRows = true;
            } else {
                row.style.display = 'none';
            }
        });

        // Если видимых строк нет, показываем сообщение "Данных нет"
        if (!hasVisibleRows) {
            noDataMessage.style.display = '';
        } else {
            noDataMessage.style.display = 'none';
        }
    });

    // Обработчик для очистки поля поиска (если потребуется сбросить фильтрацию)
    searchInput.addEventListener('blur', function () {
        if (searchInput.value === '') {
            const rows = tableBody.querySelectorAll('tr:not(:last-child)');
            rows.forEach(function (row) {
                row.style.display = ''; // Показываем все строки
            });
            resetHighlight(); // Сбрасываем подсветку
            noDataMessage.style.display = 'none';
        }
    });
});