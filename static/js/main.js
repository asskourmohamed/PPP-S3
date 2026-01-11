// main.js - Scripts globaux pour LSF Connect

document.addEventListener('DOMContentLoaded', function() {
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            if (email) {
                alert('Merci de votre inscription à notre newsletter !');
                this.reset();
            }
        });
    }

    // Active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath ||
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });

    // Toast notifications
    const messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(() => {
            messages.style.opacity = '0';
            setTimeout(() => messages.remove(), 500);
        }, 5000);
    }
});