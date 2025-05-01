// static/books/js/search.js
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  const items = Array.from(document.querySelectorAll('#book-list li'));

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLowerCase();
    items.forEach(item => {
      const title = item.querySelector('.book-title')?.textContent.toLowerCase() || '';
      const author = item.querySelector('.book-author')?.textContent.toLowerCase() || '';
      item.style.display = (title + ' ' + author).includes(query) ? '' : 'none';
    });
  });
});