import os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key-12345')

# Дані профілю
PROFILE = {
    "name": "Олег Новосад",
    "title": "Software Engineer & Python Developer",
    "bio": (
        "Привіт! Я захоплююся створенням надійних веб-сервісів, автоматизацією "
        "та дослідженням нових технологій. Працюю з Python, Flask/FastAPI, сучасним вебом та хмарними сервісами."
    ),
    "location": "Київ, Україна",
    "email": "oleg@example.com",
    "github": "https://github.com/olegnovosad",
    "linkedin": "https://linkedin.com/in/olegnovosad",
    "telegram": "https://t.me/olegnovosad",
}

# Навички
SKILLS = [
    {"category": "Backend", "skills": ["Python", "Flask", "FastAPI", "PostgreSQL", "Redis", "REST APIs"]},
    {"category": "Frontend & Tools", "skills": ["HTML5", "CSS3", "JavaScript", "Git", "Docker", "Linux"]},
    {"category": "Практики", "skills": ["Clean Architecture", "Unit Testing", "CI/CD", "Agile/Scrum"]},
]

# Проєкти
PROJECTS = [
    {
        "title": "Task Flow App",
        "description": "Веб-додаток для керування командними завданнями та аналітики продуктивності з підтримкою реального часу.",
        "tags": ["Python", "Flask", "PostgreSQL", "Docker"],
        "link": "#",
        "github": "https://github.com/olegnovosad",
    },
    {
        "title": "Data Insights Dashboard",
        "description": "Інтерактивна панель моніторингу метрик та генерації звітів для e-commerce платформи.",
        "tags": ["Python", "FastAPI", "Chart.js", "Redis"],
        "link": "#",
        "github": "https://github.com/olegnovosad",
    },
    {
        "title": "Personal Web Portal",
        "description": "Легкий та швидкий персональний сайт-візитка на Flask з підтримкою адаптивного дизайну.",
        "tags": ["Flask", "HTML5", "CSS3", "Jinja2"],
        "link": "#",
        "github": "https://github.com/olegnovosad",
    },
]

@app.context_processor
def inject_global_data():
    """Додає загальні дані профілю у всі шаблони."""
    return {"profile": PROFILE}

@app.route("/")
def index():
    return render_template("index.html", skills=SKILLS, featured_projects=PROJECTS[:2])

@app.route("/about")
def about():
    return render_template("about.html", skills=SKILLS)

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Будь ласка, заповніть усі поля форми.", "error")
        else:
            # Тут можна підключити відправку пошти або збереження в БД
            flash(f"Дякую, {name}! Ваше повідомлення успішно надіслано.", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
