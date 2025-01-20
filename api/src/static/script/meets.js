// переключение на вторую таблицу
function toggleTableStyle2() {
    const tableStyle1 = document.getElementById('table-style-1');
    const tableStyle2 = document.getElementById('table-style-2');
    const style1Button = document.getElementById('style1-button');
    const style2Button = document.getElementById('style2-button');

    tableStyle1.classList.toggle('hidden');
    tableStyle2.classList.toggle('hidden');
    style1Button.classList.toggle('active-button');
    style2Button.classList.toggle('active-button');
    style1Button.classList.toggle('inactive-button');
    style2Button.classList.toggle('inactive-button');
    style2Button.querySelector('svg').classList.toggle('fill-[#40454D]');
    style1Button.querySelector('svg').classList.toggle('fill-[#FCFEFF]');
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
    const clearErrors = () => {
    form.querySelectorAll('.error-message, .general-error, .network-error').forEach(el => el.remove());
    form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    };
    let submitButton = form.querySelector('button[type="submit"]');

    // Открытие модального окна для создания мита
    if (openModalButton) {
        clearErrors();
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
            clearErrors(); // Очищаем предыдущие ошибки
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
                    modal.classList.add('hidden');
                    location.reload();
                } else {
                    // Обработка ошибок
                    if (data.errors) {
                        // Ошибки валидации формы
                        console.error('Ошибки валидации:', data.errors);
                        // Здесь можно добавить код для отображения ошибок в форме
                        Object.entries(data.errors).forEach(([fieldName, errors]) => {
                            const field = form.querySelector(`[name="${fieldName}"]`);
                            if (field) {
                                // Добавляем класс ошибки к полю
                                field.classList.add('error');
                                // Создаем и показываем сообщение об ошибке
                                const errorDiv = document.createElement('div');
                                errorDiv.className = 'error-message';
                                errorDiv.textContent = errors.join(', ');
                                field.parentNode.appendChild(errorDiv);
                            }
                        });
                    } else if (data.message) {
                        // Ошибка от сервиса
                        console.error('Ошибка сервиса:', data.message);
                        // Можно показать общее сообщение об ошибке
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'general-error';
                        errorDiv.textContent = data.message;
                        form.insertBefore(errorDiv, form.firstChild);
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка сети:', error);
                // Показать общее сообщение об ошибке сети
                const errorDiv = document.createElement('div');
                errorDiv.className = 'network-error';
                errorDiv.textContent = 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.';
                form.insertBefore(errorDiv, form.firstChild);
            });
        });
    }
});

// редактирование мита
document.addEventListener('DOMContentLoaded', function () {
    const editMeetButtons = document.querySelectorAll('.edit-meet-button');
    const modal = document.getElementById('modal-create-meet');
    const form = document.getElementById('create-meet-form');
    const errorMessageContainer = document.getElementById('error-message'); // Контейнер для отображения ошибок
    const formFields = form.querySelectorAll('input, select, button:not(#cancel-meet)'); // Все поля формы, кроме кнопки "Отмена"

    let submitButton = form.querySelector('button[type="submit"]');

    editMeetButtons.forEach(button => {
        button.addEventListener('click', function () {
            const meetId = this.getAttribute('data-meet-id');

            // Очищаем предыдущие ошибки
            if (errorMessageContainer) {
                errorMessageContainer.textContent = '';
                errorMessageContainer.classList.add('hidden');
            }

            // Скрываем все поля формы
            formFields.forEach(field => field.classList.add('hidden'));

            // Загружаем данные мита через fetch
            fetch(`/meets/edit/${meetId}/`)
                .then(response => {
                    if (response.status === 403) {
                        // Если доступ запрещён (403), выбрасываем ошибку
                        return response.json().then(errorData => {
                            throw new Error(errorData.message || 'Доступ запрещён');
                        });
                    }
                    if (!response.ok) {
                        // Если статус ответа не 200, выбрасываем ошибку
                        throw new Error('Ошибка при загрузке данных мита');
                    }
                    return response.json();
                })
                .then(data => {
                    // Открываем модальное окно только если данные успешно получены
                    modal.classList.remove('hidden');

                    // Показываем все поля формы
                    formFields.forEach(field => field.classList.remove('hidden'));

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
                    form.setAttribute('action', `/meets/edit/${meetId}/`);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
                })
                .catch(error => {
                    console.error('Ошибка:', error);

                    // Отображаем ошибку пользователю в модальном окне
                    if (errorMessageContainer) {
                        errorMessageContainer.textContent = error.message;
                        errorMessageContainer.classList.remove('hidden');
                    }

                    // Открываем модальное окно пустым при любой ошибке
                    modal.classList.remove('hidden');
                    form.reset(); // Очищаем форму

                    // Скрываем все поля формы, кроме кнопки "Отмена"
                    formFields.forEach(field => field.classList.add('hidden'));
                });
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
            if (!response.ok) {
                        // Если ответ не OK, пытаемся прочитать JSON с ошибкой
                        return response.json().then(errorData => {
                            throw new Error(errorData.message || 'Ошибка при удалении инвайта');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === "success") {
                        console.log(`Meet with ID: ${meetId} deleted successfully.`);
                        buttonElement.closest('tr').remove();
                    } else {
                        // Обработка случая, когда статус не "success"
                        throw new Error(data.message || 'Ошибка при удалении мита');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert(error.message); // Показываем пользователю сообщение об ошибке
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

// Добавление новой категории
document.addEventListener('DOMContentLoaded', function () {
    const openCategoryModalButton = document.getElementById('open-add-category-modal');
    const closeCategoryModalButton = document.getElementById('cancel-add-category');
    const categoryModal = document.getElementById('modal-add-category');
    const categoryForm = document.getElementById('add-category-form');
    const categorySelect = document.getElementById('category');

    // Открытие модального окна для добавления категории
    openCategoryModalButton.addEventListener('click', function (e) {
        e.preventDefault();
        categoryModal.classList.remove('hidden');
    });

    // Закрытие модального окна для добавления категории
    closeCategoryModalButton.addEventListener('click', function () {
        categoryModal.classList.add('hidden');
        categoryForm.reset(); // Сбрасываем форму при закрытии
    });

    // Обработка отправки формы добавления категории
    categoryForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const categoryName = document.getElementById('category-name').value;
        const url = categoryForm.action;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'category_name': categoryName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const option = new Option(data.category_name, data.category_id);
                categorySelect.add(option);
                categorySelect.value = data.category_id;

                categoryModal.classList.add('hidden');
                categoryForm.reset();
            } else {
                alert('Ошибка при добавлении категории: ' + (data.error || 'Неизвестная ошибка'));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке формы');
        });
    });
});



// Обработка поиска
function handleSearch(event) {
    tableConfig.searchTerm = event.target.value.toLowerCase();
    tableConfig.currentPage = 1;
}
