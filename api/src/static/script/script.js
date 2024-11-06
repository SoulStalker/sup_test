document.getElementById('sidebar-toggle').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebar');
    const isCollapsed = sidebar.classList.contains('w-16');
    sidebar.classList.toggle('w-16', !isCollapsed);
    sidebar.classList.toggle('w-48', isCollapsed);

    document.querySelectorAll('.sidebar-text').forEach(el => {
        el.classList.toggle('hidden', !isCollapsed);
    });
});

// Скрипт для управления модальным окном
const modal = document.getElementById('modal');
const openModalBtn = document.getElementById('open-modal');
const closeModalBtn = document.getElementById('close-modal');


openModalBtn.addEventListener('click', () => {
    modal.classList.remove('hidden');
    modal.classList.add('modal-active');
    document.body.classList.add('modal-open');
});

closeModalBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
    modal.classList.remove('modal-active');
    document.body.classList.remove('modal-open');
});

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.classList.add('hidden');
        modal.classList.remove('modal-active');
        document.body.classList.remove('modal-open');
    }
});



document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('#container > div');

    items.forEach(item => {
        item.addEventListener('click', () => {
            items.forEach(i => i.classList.remove('active-1', 'active-2', 'active-3')); // Убираем все активные классы у всех элементов

            // Определяем активный класс для нажатого элемента
            if (item.id === 'item1') {
                item.classList.add('active-1');
            } else if (item.id === 'item2') {
                item.classList.add('active-2');
            } else if (item.id === 'item3') {
                item.classList.add('active-3');
            }
        });
    });
});

// Скрипт для кастомного множественного выбора
const selectContainer = document.getElementById('select-container');
const selectItems = document.getElementById('select-items');
const selectElement = document.getElementById('project-participants');

selectContainer.addEventListener('click', () => {
    selectContainer.classList.toggle('active');
    selectItems.classList.toggle('visible-menu');
});

selectItems.addEventListener('click', (event) => {
    if (event.target.tagName === 'DIV') {
        const value = event.target.getAttribute('data-value');
        const option = Array.from(selectElement.options).find(option => option.value === value);
        if (option) {
            option.selected = !option.selected;
            event.target.classList.toggle('selected');
        }
        selectContainer.textContent = Array.from(selectElement.options)
            .filter(option => option.selected)
            .map(option => option.text)
            .join(', ') || 'Выберите участников';
    }
});

window.addEventListener('click', (event) => {
    if (!selectContainer.contains(event.target) && !selectItems.contains(event.target)) {
        selectItems.classList.remove('visible-menu');
        selectContainer.classList.remove('active');
    }
});

// Скрипт для управления попапом подтверждения удаления
const confirmDeletePopup = document.getElementById('confirm-delete-popup');
const deleteProjectBtn = document.getElementById('delete-project');
const confirmDeleteBtn = document.getElementById('confirm-delete');
const cancelDeleteBtn = document.getElementById('cancel-delete');

deleteProjectBtn.addEventListener('click', () => {
    confirmDeletePopup.classList.remove('hidden');
});

cancelDeleteBtn.addEventListener('click', () => {
    confirmDeletePopup.classList.add('hidden');
});

confirmDeleteBtn.addEventListener('click', () => {
    // Здесь можно добавить код для удаления проекта
    confirmDeletePopup.classList.add('hidden');
});

confirmDeletePopup.addEventListener('click', (event) => {
    if (event.target === confirmDeletePopup) {
        confirmDeletePopup.classList.add('hidden');
    }
});


// Скрипт для управления модальным окном
document.addEventListener('DOMContentLoaded', () => {
    const newModal = document.getElementById('new-modal');
    const openNewModalBtn = document.getElementById('open-new-modal'); // Добавьте элемент для открытия модального окна в HTML
    const closeNewModalBtn = document.getElementById('close-new-modal');

    // Проверяем, что элементы существуют
    if (!newModal || !openNewModalBtn || !closeNewModalBtn) {
        console.error('Не удалось найти один или несколько элементов');
        return;
    }

    // Функция для открытия модального окна
    function openNewModal() {
        newModal.classList.remove('hidden');
        newModal.classList.add('modal-active');
        document.body.classList.add('modal-open');
    }

    // Функция для закрытия модального окна
    function closeNewModal() {
        newModal.classList.add('hidden');
        newModal.classList.remove('modal-active');
        document.body.classList.remove('modal-open');
    }

    // Добавляем обработчики событий
    openNewModalBtn.addEventListener('click', openNewModal);
    closeNewModalBtn.addEventListener('click', closeNewModal);

    // Закрытие модального окна при клике вне его содержимого
    window.addEventListener('click', (event) => {
        if (event.target === newModal) {
            closeNewModal();
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const contentFitch = document.querySelector('.content-fitch');

    function adjustContentFitch() {
        const viewportHeight = window.innerHeight;
        const scrollPosition = window.scrollY;

        // Устанавливаем высоту элемента, чтобы она была видна после 60% высоты экрана
        if (scrollPosition > (0.6 * viewportHeight)) {
            contentFitch.style.maxHeight = '100vh'; // Расширяем элемент на всю высоту экрана
        } else {
            contentFitch.style.maxHeight = '60vh'; // Устанавливаем высоту 60% экрана
        }
    }

    // Добавляем обработчик события прокрутки
    window.addEventListener('scroll', adjustContentFitch);
});
