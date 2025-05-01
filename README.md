# Book Manager

A Django-based application for managing a personal library of books. Provides both a web interface and a RESTful API (using Django REST Framework) with features such as CRUD operations, rating, daily featured book, search, authentication, and pagination.

## 🚀 Features

- **User registration & login** (Django Auth)
- **CRUD** for books: add, view, edit, delete
- **Book of the Day**: random daily recommendation with caching
- **Rating system**: submit and view average ratings via AJAX
- **Client-side search**: real-time filtering of book list
- **REST API**: full Create, Read, Update, Delete endpoints with pagination and permissions
- **Responsive design**: modern UI with custom CSS
- **Unit tests**: coverage for models, views, API, and caching logic

## 🛠 Tech Stack

- Python 3.13
- Django 5.1
- Django REST Framework
- HTML5, CSS3
- JavaScript (ES6)
- SQLite (development)
- Git & GitHub

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<YOUR_USERNAME>/book-manager.git
   cd book-manager
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   The project uses `DJANGO_SECRET_KEY` for security in production, with a default fallback for local development. Create a `.env` file in the project root with:
   ```env
   DJANGO_SECRET_KEY=your-production-secret-key
   DEBUG=True
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ``` **Run the development server**

   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000/` in your browser.

## 🔌 API Endpoints

- **API Root**: `GET /api/`
- **List/Create Books**: `GET, POST /api/books/`
- **Retrieve/Update/Delete Book**: `GET, PUT, PATCH, DELETE /api/books/{id}/`

Example: fetch list of books

```bash
curl -i http://localhost:8000/api/books/
```

## 🔑 Authentication & Permissions

- Unauthenticated users can **view** books and the API list.
- Only authenticated users can **create**, **update**, or **delete** books via the API.
- Rating via AJAX on the front end does not require login (customizable).

## 🧪 Running Tests

```bash
python manage.py test
```

## 📂 Project Structure

```
book_manager/       # project root
├── books/          # app containing models, views, templates, tests
├── book_manager/   # project settings and URLs
├── static/         # global static files
├── templates/      # global templates
├── media/          # uploaded book cover images
├── manage.py       # Django management script
└── requirements.txt
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request


