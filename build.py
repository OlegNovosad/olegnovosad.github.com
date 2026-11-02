#!/usr/bin/env python3
"""
Скрипт збирання статичного сайту з Flask-додатку для GitHub Pages.
Генерує готові HTML-файли та копіює статику в папку dist/.
"""

import os
import re
import shutil
from app import app

OUTPUT_DIR = "dist"

PAGES = [
    ("/", "index.html"),
    ("/about", "about.html"),
    ("/projects", "projects.html"),
    ("/contact", "contact.html"),
    ("/404", "404.html"),
]

def make_relative(html_content: str, depth: int = 0) -> str:
    """Робить абсолютні посилання у згенерованому HTML відносними для підтримки будь-яких URL на GitHub Pages."""
    prefix = "../" * depth if depth > 0 else "./"
    
    # Заміна посилань на статику (/static/ -> ./static/ або ../static/)
    content = re.sub(r'(href|src)=["\']/static/', rf'\1="{prefix}static/', html_content)
    
    # Заміна внутрішніх маршрутів на відповідні html файли
    content = re.sub(r'href=["\']/(about|projects|contact)["\']', rf'href="{prefix}\1.html"', content)
    content = re.sub(r'href=["\']/(about|projects|contact)/["\']', rf'href="{prefix}\1.html"', content)
    content = re.sub(r'href=["\']/["\']', rf'href="{prefix}index.html"', content)
    
    return content

def build():
    print(f"🚀 Початок збирання статичного сайту в папку '{OUTPUT_DIR}'...")
    
    # Очищення та створення цільової папки
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Копіювання статичних файлів (CSS, JS, зображення)
    if os.path.exists("static"):
        shutil.copytree("static", os.path.join(OUTPUT_DIR, "static"))
        print("  ✓ Скопійовано папку static/")

    # Файл .nojekyll повідомляє GitHub Pages не обробляти сайт через Jekyll
    with open(os.path.join(OUTPUT_DIR, ".nojekyll"), "w") as f:
        f.write("")
    print("  ✓ Створено .nojekyll")

    # Рендеринг кожної сторінки через тестовий клієнт Flask
    client = app.test_client()

    for route, filename in PAGES:
        response = client.get(route)
        if response.status_code not in (200, 404):
            print(f"  ❌ Помилка рендерингу {route}: код {response.status_code}")
            continue

        raw_html = response.get_data(as_text=True)

        # 1. Збереження у корінь (наприклад: dist/about.html)
        dest_file = os.path.join(OUTPUT_DIR, filename)
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(make_relative(raw_html, depth=0))
        print(f"  ✓ Згенеровано: {filename}")

        # 2. Збереження у підпапку (dist/about/index.html) для підтримки красивих URL без .html
        if filename != "index.html" and filename != "404.html":
            folder_name = filename.replace(".html", "")
            folder_path = os.path.join(OUTPUT_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(make_relative(raw_html, depth=1))
            print(f"  ✓ Згенеровано: {folder_name}/index.html")

    # Також створюємо копію в папці docs/ для підтримки налаштування GitHub Pages "Deploy from a branch -> /docs"
    docs_dir = "docs"
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    shutil.copytree(OUTPUT_DIR, docs_dir)
    print("  ✓ Синхронізовано з папкою docs/ (для режиму 'Deploy from /docs')")

    print("\n✨ Збирання успішно завершено! Файли готові до публікації на GitHub Pages.")

if __name__ == "__main__":
    build()
