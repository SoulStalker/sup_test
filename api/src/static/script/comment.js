document.addEventListener('DOMContentLoaded', function () {
    const openCommentModalButton = document.querySelectorAll('.open-comment-modal'); // Кнопки для открытия модального окна комментариев
    const closeCommentModalButton = document.getElementById('close-comment-modal');
    const commentModal = document.getElementById('comment-modal');
    const commentForm = document.getElementById('comment-form');

    // Закрытие модального окна
    function closeCommentModal() {
        commentModal.classList.add('hidden');
        commentForm.reset(); // Сбрасываем форму
    }

    // Открытие модального окна для добавления комментария
    openCommentModalButton.forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.getAttribute('data-task-id'); // Получаем ID задачи
            commentModal.classList.remove('hidden');
            document.getElementById('comment-task-id').value = taskId; // Устанавливаем ID задачи в скрытое поле
            commentForm.reset(); // Сбрасываем форму
        });
    });

    // Закрытие модального окна
    closeCommentModalButton.addEventListener('click', closeCommentModal);

    // Обработка отправки формы комментариев
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('Отправка формы комментария');

        const formData = new FormData(commentForm);
        console.log('Данные комментария:', Array.from(formData.entries()));

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
                console.log('Закрытие модального окна');
                closeCommentModal(); // Закрываем модальное окно при успешном ответе
                location.reload(); // Перезагрузка страницы для обновления данных
            } else {
                // Обработка ошибок
                if (data.errors) {
                    console.error('Ошибки валидации:', data.errors);
                    // Обработка ошибок аналогично тому, как это сделано в форме задачи
                } else if (data.message) {
                    console.error('Ошибка сервиса:', data.message);
                    // Обработка общего сообщения об ошибке
                }
            }
        })
        .catch(error => {
            console.error('Ошибка сети:', error);
            // Обработка сетевой ошибки
        });
    });
    document.querySelectorAll('.edit-comment').forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.getAttribute('data-comment-id');
    
            // Запрос старого комментария
            fetch(`/projects/features/tasks/comment/update/${commentId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.comment) {
                        document.getElementById('comment-text').value = data.comment; // Автозаполнение старым текстом
                        document.getElementById('comment-task-id').value = commentId; // Устанавливаем ID комментария
                        commentModal.classList.remove('hidden'); // Открываем модальное окно
                    }
                })
                .catch(error => {
                    console.error('Ошибка при получении комментария:', error);
                });
        });
    });
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const commentId = document.getElementById('comment-task-id').value; // Получаем ID комментария
    
        const formData = new FormData(commentForm);
        const url = commentId ? `/projects/features/tasks/comment/update/${commentId}/` : commentForm.action; // Используем правильный URL
    
        fetch(url, {
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
                closeCommentModal(); // Закрываем модальное окно при успешном ответе
                location.reload(); // Перезагрузка страницы для обновления данных
            } else {
                // Обработка ошибок
                console.error('Ошибки:', data.errors);
            }
        })
        .catch(error => {
            console.error('Ошибка сети:', error);
        });
    });
});