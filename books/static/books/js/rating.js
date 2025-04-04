document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('submit-rating');
    if (!submitButton) return;

    submitButton.addEventListener('click', function() {
        var select = document.getElementById('rating-select');
        var rating = select.value;
        if (!rating) {
            alert('Будь ласка, оберіть оцінку.');
            return;
        }
        
        // Отримання URL з data-атрибуту кнопки
        var url = submitButton.getAttribute('data-url');

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        // Отримання CSRF токену (припускаємо, що він встановлений як cookie)
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Чи починається cookie з потрібного імені?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrfToken = getCookie('csrftoken');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                // Оновлення середнього рейтингу на сторінці
                document.getElementById('avg-rating').textContent = response.average_rating;
            } else {
                alert('Помилка при надсиланні оцінки.');
            }
        };

        xhr.send('rating=' + encodeURIComponent(rating));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const ratingBox = document.querySelector('.rating-stars');
    if (!stars.length || !ratingBox) return;

    const csrfToken = document.querySelector('form input[name=csrfmiddlewaretoken]').value;
    const avgRating = document.getElementById('avg-rating');
    const url = ratingBox.dataset.url;

    stars.forEach(star => {
        star.addEventListener('mouseover', function () {
            const val = parseInt(this.dataset.value);
            highlightStars(val);
        });

        star.addEventListener('mouseout', function () {
            const selected = parseInt(ratingBox.dataset.selected || 0);
            highlightStars(selected);
        });

        star.addEventListener('click', function () {
            const val = parseInt(this.dataset.value);
            ratingBox.dataset.selected = val;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: `rating=${val}`
            })
            .then(res => res.json())
            .then(data => {
                avgRating.textContent = data.average_rating;
            });

            highlightStars(val);
        });
    });

    function highlightStars(rating) {
        stars.forEach(star => {
            const val = parseInt(star.dataset.value);
            if (val <= rating) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }
});