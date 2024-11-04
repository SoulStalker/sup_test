document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal");                // Модальное окно
    const openModalCreateBtn = document.getElementById("open-modal-create");  // Кнопка "Создать фичу"
    const closeModalBtn = document.getElementById("close-modal");  // Кнопка закрытия модального окна
    const form = document.getElementById("create-project-form");   // Форма создания фичи

    let isEditMode = false;      // Флаг, указывающий, редактирование ли это или создание новой фичи
    let featureId = null;        // ID фичи для редактирования (если есть)

    // Функция для открытия модального окна в режиме создания новой фичи
    openModalCreateBtn.addEventListener("click", function () {
        isEditMode = false;           // Устанавливаем режим создания новой фичи
        featureId = null;             // Сбрасываем ID фичи, т.к. создаем новую
        form.reset();                 // Очищаем форму
        modal.classList.remove("hidden");  // Показываем модальное окно
    });

    // Функция для закрытия модального окна
    closeModalBtn.addEventListener("click", function () {
        modal.classList.add("hidden");  // Прячем модальное окно
    });

    // Закрытие модального окна при клике вне его области
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.classList.add("hidden");
        }
    });

    // Функция для загрузки данных о фиче для редактирования
    function loadFeatureData(featureId) {
        fetch(`/projects/features/edit/${featureId}/`)  // URL для запроса данных фичи (замените на свой маршрут)
            .then(response => response.json()) // Преобразуем ответ в JSON
            .then(data => {
                // Заполняем форму данными фичи
                document.getElementById("project-name").value = data.name;
                document.getElementById("project-responsible").value = data.responsible;
                document.getElementById("project-description").value = data.description;
                document.getElementById("project-tags").value = data.tags;
                document.getElementById("project-importance").value = data.importance;
                document.getElementById("project-status").value = data.status;
                document.getElementById("project-project").value = data.project;

                isEditMode = true;          // Устанавливаем режим редактирования
                modal.classList.remove("hidden");  // Показываем модальное окно
            })
            .catch(error => console.error("Ошибка при загрузке данных фичи:", error));
    }

    // Открытие формы для редактирования существующей фичи
    document.querySelectorAll(".open-modal-btn[data-feature-id]").forEach(button => {
        button.addEventListener("click", function () {
            featureId = this.dataset.featureId;   // Получаем ID фичи из data-атрибута кнопки
            loadFeatureData(featureId);           // Загружаем данные фичи
        });
    });

    // Обработка отправки формы
    form.addEventListener("submit", function (event) {
        event.preventDefault();  // Предотвращаем отправку формы по умолчанию

        const formData = new FormData(form); // Создаем объект FormData из формы

        // Устанавливаем URL для отправки данных
        const url = isEditMode ? `/projects/features/edit/${featureId}/` : `/projects/features/create/`;

        // Отправляем данные на сервер
        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Ожидаем JSON-ответ
            }
            throw new Error("Ошибка при отправке формы.");
        })
        .then(data => {
            console.log("Фича успешно создана или обновлена:", data);
            modal.classList.add("hidden");  // Закрываем модальное окно
            form.reset();                    // Очищаем форму
            // Здесь можно добавить код для обновления списка фич на странице
        })
        .catch(error => console.error("Ошибка:", error));
    });
});
