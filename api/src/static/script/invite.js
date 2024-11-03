const openModalButton = document.getElementById('open-modal');
const url = openModalButton.getAttribute('data-url');

openModalButton.addEventListener('click', () => {
  // Send a POST request to the invite
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')  // Добавлено для CSRF
    },
    body: JSON.stringify({
      // Добавьте необходимые данные, которые нужно отправить на сервер
    }),
  })
  .then(response => response.json())
  .then(data => console.log(data))
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
