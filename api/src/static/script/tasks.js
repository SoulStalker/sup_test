document.addEventListener('DOMContentLoaded', function () {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modal = document.getElementById('modal');
    const form = document.getElementById('create-task-form');
    const modalTitle = document.getElementById('modal-title'); // Заголовок модального окна
    const deleteButton = document.getElementById('delete-task-button'); // Кнопка удаления
    const confirmDeletePopup = document.getElementById('confirm-delete-popup'); // Попап подтверждения удаления
    const confirmDeleteButton = document.getElementById('confirm-delete'); // Кнопка подтверждения удаления
    const accessDeniedPopup = document.getElementById('access-denied-popup');
    const accessDeniedMessage = document.getElementById('access-denied-message');
    const closeAccessDeniedPopup = document.getElementById('close-access-denied-popup');
    const tagsContainer = document.getElementById('tags-container');
    const tagsInput = document.getElementById('task-tags'); // Поле для хранения выбранных тегов

    let submitButton = form.querySelector('button[type="submit"]');
    let currentTaskId = null; // Переменная для хранения текущего ID задачи
    let editor = null;
    let selectedTags = []; // Массив для хранения ID выбранных тегов

    function initEditor() {
        if (editor) return; // Уже инициализирован

        ClassicEditor
            .create(document.querySelector('#task-description'))
            .then(newEditor => {
                editor = newEditor;
            })
            .catch(error => {
                console.error('Ошибка инициализации CKEditor:', error);
            });
    }

    // Открытие модального окна для создания задачи
    if (openModalButton) {
        openModalButton.addEventListener('click', function () {
            modal.classList.remove('hidden');
            modalTitle.textContent = 'Создание задачи'; // Устанавливаем заголовок для создания задачи
            initEditor();
            form.setAttribute('action', 'create/');
            submitButton.textContent = 'Создать задачу';
            form.reset();
            clearErrors(); // Очистить ошибки при открытии окна
        });
    }

    // Закрытие модального окна
    function closeModal() {
        if (editor) {
            editor.setData(''); // Очищаем содержимое
        }
        modal.classList.add('hidden');
        form.reset(); // Сбрасываем форму
        clearErrors(); // Очищение ошибок
    }

    // Обработчик клика по кнопке закрытия модального окна
    closeModalButton.addEventListener('click', closeModal);
    document.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal(); // Закрываем модальное окно при клике вне него
        }
    });

    // Обработка отправки формы
    form.addEventListener('submit', function (event) {
        if (editor) {
            editor.updateSourceElement(); // Синхронизируем данные
        }
        event.preventDefault();
        console.log('Отправка формы создания задачи');

        // Проверка валидности формы
        if (!form.checkValidity()) {
            console.error('Форма невалидна. Пожалуйста, проверьте введенные данные.');
            return;
        }

        const formData = new FormData(form);
        console.log('Данные формы:', Array.from(formData.entries()));

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => {
                console.log('Ответ от сервера:', response);
                if (!response.ok) {
                    throw new Error('Сеть ответила с ошибкой: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                console.log('Данные от сервера:', data);
                if (data.status === 'success') {
                    closeModal(); // Закрываем модальное окно при успешном ответе
                    location.reload(); // Перезагрузка страницы для обновления данных
                } else {
                    // Обработка ошибок
                    if (data.errors) {
                        console.error('Ошибки валидации:', data.errors);
                        Object.entries(data.errors).forEach(([fieldName, errors]) => {
                            const field = form.querySelector(`[name="${fieldName}"]`);
                            if (field) {
                                showError(field, errors);
                            }
                        });
                    } else if (data.message) {
                        console.error('Ошибка сервиса:', data.message);
                        const generalErrorDiv = document.createElement('div');
                        generalErrorDiv.className = 'general-error';
                        generalErrorDiv.textContent = data.message;
                        form.insertBefore(generalErrorDiv, form.firstChild);
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка сети:', error);
                const networkErrorDiv = document.createElement('div');
                networkErrorDiv.className = 'network-error';
                networkErrorDiv.textContent = 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.';
                form.insertBefore(networkErrorDiv, form.firstChild);
            });
    });

    // Редактирование задачи
    const editTaskButtons = document.querySelectorAll('.edit-task-button');
    editTaskButtons.forEach(button => {
        button.addEventListener('click', function () {
            currentTaskId = this.getAttribute('data-task-id'); // Получаем ID задачи
            const editUrl = this.getAttribute('data-url');
            // Инициализация редактора перед заполнением данных
            initEditor(); // Добавлено здесь
            fetch(editUrl)
                .then(response => {
                    if (response.status === 403) {
                        // Если доступ запрещён (403), показываем попап с ошибкой
                        return response.json().then(errorData => {
                            accessDeniedMessage.textContent = errorData.message || 'Доступ запрещён';
                            accessDeniedPopup.classList.remove('hidden');
                            throw new Error(errorData.message || 'Доступ запрещён');
                        });
                    }
                    if (!response.ok) {
                        return response.json().then(errData => {
                            throw new Error(`Ошибка ${response.status}: ${errData.message || 'Неизвестная ошибка'}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    // Заполняем форму полученными данными
                    document.getElementById('task-name').value = data.name || '';
                    document.getElementById('task-priority').value = data.priority || '';
                    if (editor) {
                        editor.setData(data.description || ''); // Устанавливаем данные
                    }
                    document.getElementById('task-status').value = data.status || '';
                    document.getElementById('task-responsible').value = data.responsible || '';
                    document.getElementById('task-feature').value = data.feature || '';
                    document.getElementById('task-contributor').value = data.contributor || '';

                    // Логика выделения тегов
                    const tags = document.querySelectorAll('.tag'); // Все элементы тегов
                    const selectedTagsFromServer = data.tags || []; // ID выбранных тегов
                    document.task_id = data.id || null;

                    // Очищаем все выделения
                    tags.forEach(tag => {
                        tag.classList.remove('selected');
                    });

                    // Обновляем массив выбранных тегов
                    selectedTags = [];
                    selectedTagsFromServer.forEach(tagId => {
                        const tagElement = document.querySelector(`.tag[data-tag-id="${tagId}"]`);
                        if (tagElement) {
                            tagElement.classList.add('selected'); // Добавляем класс "selected"
                            selectedTags.push(tagId); // Добавляем в массив
                        }
                    });

                    // Обновляем значение скрытого поля
                    tagsInput.value = selectedTags.join(',');

                    // Устанавливаем заголовок для редактирования задачи
                    modalTitle.textContent = 'Редактирование задачи';

                    modal.classList.remove('hidden');
                    form.setAttribute('action', editUrl);
                    submitButton.textContent = 'Сохранить'; // Меняем текст кнопки на "Сохранить"
                })
                .catch(error => console.error('Ошибка:', error));
            // Обработчик закрытия попапа с ошибкой доступа
            closeAccessDeniedPopup.addEventListener('click', function () {
                accessDeniedPopup.classList.add('hidden');
            });
        });
    });

    // Обработчик для открытия попапа подтверждения удаления
    deleteButton.addEventListener('click', function () {
        currentTaskId = this.getAttribute('data-task-id'); // Устанавливаем currentTaskId
        console.log("Открытие попапа подтверждения удаления");
        console.log("ID задачи для удаления:", document.task_id);
        confirmDeletePopup.classList.remove('hidden'); // Показываем попап подтверждения удаления
    });

    // Обработчик подтверждения удаления задачи
    confirmDeleteButton.addEventListener('click', function () {
        console.log("Подтверждение удаления задачи");
        console.log("ID задачи для удаления:", document.task_id);
        if (document.task_id) {
            fetch(`delete/${document.task_id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        confirmDeletePopup.classList.add('hidden'); // Закрываем попап подтверждения удаления
                        closeModal(); // Закрываем модальное окно редактирования
                        window.location.reload(); // Это обновит текущую страницу
                    } else {
                        alert('Ошибка: ' + data.message); // Показываем сообщение об ошибке
                    }
                })
                .catch(error => console.error('Ошибка при удалении задачи:', error));
        }
    });

    // Обработчик отмены удаления задачи
    const cancelDeleteButton = document.getElementById('cancel-delete'); // Кнопка отмены удаления
    cancelDeleteButton.addEventListener('click', function () {
        confirmDeletePopup.classList.add('hidden'); // Скрываем попап подтверждения удаления
    });

    // Очищение ошибок формы
    const clearErrors = () => {
        console.log('Очищение ошибок формы');
        const errorDivs = form.querySelectorAll('.error');
        errorDivs.forEach(div => div.remove()); // Удаляем все сообщения об ошибках
    };

    // Функция для отображения ошибок
    const showError = (field, errors) => {
        console.error('Ошибки поля', field.name, errors);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = errors.join(', ');
        field.parentNode.insertBefore(errorDiv, field.nextSibling); // Вставляем ошибку после поля
    };

    // Обработка кликов по тегам
    tagsContainer.addEventListener('click', function (event) {
        const tagElement = event.target.closest('.tag');
        if (!tagElement) return; // Если клик не на теге, выход

        const tagId = tagElement.getAttribute('data-tag-id');

        if (tagElement.classList.contains('selected')) {
            // Убираем тег из выбранных
            tagElement.classList.remove('selected');
            selectedTags = selectedTags.filter(id => id !== tagId);
        } else {
            // Добавляем тег в выбранные
            tagElement.classList.add('selected');
            selectedTags.push(tagId);
        }

        // Обновляем значение скрытого поля
        tagsInput.value = selectedTags.join(',');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const openCommentModalButton = document.getElementById('open-comment-modal');
    const closeCommentModalButton = document.getElementById('close-comment-modal');
    const commentModal = document.getElementById('comment-modal');
    const commentForm = document.getElementById('comment-form');

    // Открытие модального окна для создания комментария
    if (openCommentModalButton) {
        openCommentModalButton.addEventListener('click', function () {
            const taskId = this.getAttribute('data-task-id');
            document.getElementById('comment-task-id').value = taskId;
            commentModal.classList.remove('hidden');
        });
    }

    // Закрытие модального окна
    closeCommentModalButton.addEventListener('click', function () {
        commentModal.classList.add('hidden');
    });

    // Обработка отправки формы комментария
    commentForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(commentForm);

        fetch(commentForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Сеть ответила с ошибкой: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    commentModal.classList.add('hidden');
                    location.reload(); // Перезагрузка страницы для обновления данных
                } else {
                    // Обработка ошибок
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([fieldName, errors]) => {
                            const field = commentForm.querySelector(`[name="${fieldName}"]`);
                            if (field) {
                                showError(field, errors);
                            }
                        });
                    } else if (data.message) {
                        const generalErrorDiv = document.createElement('div');
                        generalErrorDiv.className = 'general-error';
                        generalErrorDiv.textContent = data.message;
                        commentForm.insertBefore(generalErrorDiv, commentForm.firstChild);
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка сети:', error);
                const networkErrorDiv = document.createElement('div');
                networkErrorDiv.className = 'network-error';
                networkErrorDiv.textContent = 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.';
                commentForm.insertBefore(networkErrorDiv, commentForm.firstChild);
            });
    });

    // Функция для отображения ошибок
    const showError = (field, errors) => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = errors.join(', ');
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    };
});
