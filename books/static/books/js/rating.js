document.addEventListener('DOMContentLoaded', () => {
    const ratingBox = document.querySelector('.rating-stars');
    if (!ratingBox) return;
  
    const stars = Array.from(document.querySelectorAll('.star'));
    const avgRatingElem = document.getElementById('avg-rating');
    const url = ratingBox.dataset.url;
    // CSRF-токен беремо з мета-тега в <head>
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  
    // Встановлюємо підсвічування зірок за hover і reset
    stars.forEach(star => {
      const val = parseInt(star.dataset.value, 10);
  
      star.addEventListener('mouseover', () => highlightStars(val));
      star.addEventListener('mouseout', () => {
        const selected = parseInt(ratingBox.dataset.selected, 10) || 0;
        highlightStars(selected);
      });
  
      star.addEventListener('click', () => {
        // Зберігаємо вибране значення
        ratingBox.dataset.selected = val;
        highlightStars(val);
  
        // Відправляємо POST-запит
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
          },
          body: `rating=${val}`
        })
        .then(response => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then(data => {
          avgRatingElem.textContent = data.average_rating;
        })
        .catch(error => {
          console.error('Error submitting rating:', error);
          alert('Помилка при надсиланні оцінки. Спробуйте ще раз.');
        });
      });
    });
  
    function highlightStars(rating) {
      stars.forEach(s => {
        const v = parseInt(s.dataset.value, 10);
        s.classList.toggle('selected', v <= rating);
      });
    }
  
    // Підсвічуємо початковий стан, якщо вже є вибрана оцінка
    highlightStars(parseInt(ratingBox.dataset.selected, 10) || 0);
  });