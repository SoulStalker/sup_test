// Пагинация
document.addEventListener('DOMContentLoaded', function () {
    const rowsPerPageSelect = document.getElementById('rows-per-page');
    const rowsPerPageForm = document.getElementById('rows-per-page-form');

    rowsPerPageSelect.addEventListener('change', function () {
        // Сбрасываем номер страницы на 1 при изменении количества элементов
        const pageInput = rowsPerPageForm.querySelector('input[name="page"]');
        if (pageInput) {
            pageInput.value = '1';
        }
        rowsPerPageForm.submit();
    });
});
