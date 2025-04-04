console.log("Search script loaded!");
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const bookList = document.getElementById('book-list');
    const allBooks = Array.from(bookList.getElementsByTagName('li'));
  
    searchInput.addEventListener('input', function () {
      const query = this.value.toLowerCase();
      allBooks.forEach(function (book) {
        const text = book.textContent.toLowerCase();
        book.style.display = text.includes(query) ? '' : 'none';
      });
    });
  });