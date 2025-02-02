document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("navbar-sticky");

    // Функция для обработки события скролла
    const handleScroll = () => {
        if (window.scrollY > 0) {
            navbar.classList.add("navbar-scrolled"); // Добавляем класс при скролле
        } else {
            navbar.classList.remove("navbar-scrolled"); // Убираем класс, если на верху страницы
        }
    };

    // Добавляем слушатель события скролла
    window.addEventListener("scroll", handleScroll);
});

document.addEventListener("DOMContentLoaded", function () {
    // Находим все кнопки аккордеона
    const accordions = document.querySelectorAll(".hs-accordion-toggle");

    accordions.forEach(button => {
        button.addEventListener("click", function () {
            const content = this.nextElementSibling;
            const icon = this.querySelector("[data-lucide='chevron-up']");

            // Закрываем все остальные аккордеоны
            document.querySelectorAll(".hs-accordion-content").forEach(item => {
                if (item !== content) {
                    item.classList.add("hidden");
                    item.previousElementSibling.querySelector("[data-lucide='chevron-up']").classList.remove("-rotate-180");
                }
            });

            // Переключаем текущий аккордеон
            content.classList.toggle("hidden");
            icon.classList.toggle("-rotate-180");
        });
    });
});