// Создание приглашения
const openModalButton = document.getElementById('open-modal');
const url = openModalButton.getAttribute('data-url');

openModalButton.addEventListener('click', () => {
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      // Добавьте необходимые данные, которые нужно отправить на сервер
    }),
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("Ошибка при создании приглашения");
    }
  })
  .then(data => {
    console.log("Перед перезагрузкой", data);
    location.reload();
    console.log("После перезагрузки"); // Этот лог мы не увидим, если перезагрузка сработает
    })
  .catch(error => console.error(error));
});

// Функция для получения CSRF-токена
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


// Удаление приглашения
document.addEventListener('DOMContentLoaded', function() {
    const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMetaTag ? csrfMetaTag.getAttribute('content') : null;

    if (!csrfToken) {
        console.error("CSRF token not found in meta tag!");
        alert("CSRF token missing, please check the meta tag.");
        return;
    }

    const deleteButtons = document.querySelectorAll('.delete-btn');
    const confirmDeletePopup = document.getElementById('confirm-delete-popup');
    const confirmDeleteButton = document.getElementById('confirm-delete');
    const cancelDeleteButton = document.getElementById('cancel-delete');

    let currentInviteId = null;
    let currentDeleteButton = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentInviteId = this.getAttribute('data-invite-id');
            currentDeleteButton = this;
            confirmDeletePopup.classList.remove('hidden');
        });
    });

    confirmDeleteButton.addEventListener('click', function() {
        if (currentInviteId) {
            deleteInvite(currentInviteId, currentDeleteButton);
        }
        confirmDeletePopup.classList.add('hidden');
    });

    cancelDeleteButton.addEventListener('click', function() {
        confirmDeletePopup.classList.add('hidden');
        currentInviteId = null;
        currentDeleteButton = null;
    });

    function deleteInvite(inviteId, buttonElement) {
        console.log(`Attempting to delete invite with ID: ${inviteId}`);

        fetch(`delete/${inviteId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            console.log(`Response status: ${response.status}`);
            if (response.ok) {
                console.log(`Invite with ID: ${inviteId} deleted successfully.`);
                buttonElement.closest('tr').remove();
            } else {
                return response.text().then(text => {
                    console.error(`Error response text: ${text}`);
                    throw new Error('Ошибка при удалении инвайта');
                });
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при удалении инвайта');
        });
    }
});

// Получить ссылку в буфер обмена
document.addEventListener('DOMContentLoaded', function() {
    const copyButtons = document.querySelectorAll('.copy-invite');

    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const inviteLink = this.getAttribute('data-invite-link');

            if (inviteLink) {
                navigator.clipboard.writeText(inviteLink)
                    .then(() => {
                        console.log("Link copied to clipboard:", inviteLink);
                        alert("Ссылка скопирована в буфер обмена!");
                    })
                    .catch(error => {
                        console.error("Ошибка при копировании:", error);
                        alert("Не удалось скопировать ссылку.");
                    });
            } else {
                console.error("Link not found in data-invite-link attribute.");
            }
        });
    });
});


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
