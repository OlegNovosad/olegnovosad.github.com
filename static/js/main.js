document.addEventListener('DOMContentLoaded', () => {
    // Встановлення поточного року у футері
    const yearSpan = document.getElementById('currentYear');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // Мобільне меню (бургер)
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.getElementById('navLinks');

    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Закриття меню при кліку на посилання
        navLinks.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // Автоматичне зникнення Flash-повідомлень через 5 секунд
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = 'opacity 0.5s ease';
                msg.style.opacity = '0';
                setTimeout(() => msg.remove(), 500);
            });
        }, 5000);
    }

    // Обробка форми контактів у статичному режимі (наприклад, на GitHub Pages)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            // Перевіряємо, чи сайт запущено на GitHub Pages або статично (без бекенду)
            const isStaticHost = window.location.hostname.endsWith('github.io') ||
                                 window.location.protocol === 'file:' ||
                                 (!window.location.port && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1');

            if (isStaticHost) {
                e.preventDefault();
                const name = document.getElementById('name').value.trim();
                const email = document.getElementById('email').value.trim();
                const message = document.getElementById('message').value.trim();

                if (!name || !email || !message) {
                    alert('Будь ласка, заповніть усі поля форми.');
                    return;
                }

                // Відкриваємо поштовий клієнт з заповненими даними
                const subject = encodeURIComponent(`Повідомлення з сайту від ${name}`);
                const body = encodeURIComponent(`Ім'я: ${name}\nEmail: ${email}\n\nПовідомлення:\n${message}`);
                window.location.href = `mailto:oleg@example.com?subject=${subject}&body=${body}`;

                // Показуємо повідомлення користувачеві
                const formCard = contactForm.parentElement;
                contactForm.reset();

                const successNotice = document.createElement('div');
                successNotice.className = 'flash-message flash-success';
                successNotice.style.marginTop = '1rem';
                successNotice.innerHTML = `<span>Дякую, ${name}! Оскільки сайт працює як статичний на GitHub Pages, відкрито ваш поштовий клієнт для надсилання листа.</span>`;
                formCard.appendChild(successNotice);

                setTimeout(() => {
                    successNotice.remove();
                }, 7000);
            }
        });
    }
});

