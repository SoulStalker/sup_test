// pagination.js
document.addEventListener('DOMContentLoaded', function() {
    const meetsContainer = document.getElementById('meets-container');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    // Функция для обновления состояния кнопок
    function updatePaginationState(data) {
        prevButton.disabled = !data.has_previous;
        nextButton.disabled = !data.has_next;

        prevButton.classList.toggle('opacity-50', !data.has_previous);
        prevButton.classList.toggle('cursor-not-allowed', !data.has_previous);

        nextButton.classList.toggle('opacity-50', !data.has_next);
        nextButton.classList.toggle('cursor-not-allowed', !data.has_next);

        prevButton.dataset.page = data.current_page - 1;
        nextButton.dataset.page = data.current_page + 1;

        pageInfo.textContent = `Страница ${data.current_page} из ${data.total_pages}`;
    }

    // Функция для загрузки страницы
    async function loadPage(pageNum) {
        try {
            const response = await fetch(`?page=${pageNum}&ajax=1`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            meetsContainer.innerHTML = data.html;
            updatePaginationState(data.pagination);

            // Обновляем URL без перезагрузки страницы
            const url = new URL(window.location);
            url.searchParams.set('page', pageNum);
            window.history.pushState({}, '', url);

        } catch (error) {
            console.error('Error loading page:', error);
        }
    }

    // Обработчики для кнопок
    prevButton.addEventListener('click', function() {
        if (!this.disabled) {
            loadPage(this.dataset.page);
        }
    });

    nextButton.addEventListener('click', function() {
        if (!this.disabled) {
            loadPage(this.dataset.page);
        }
    });
});
