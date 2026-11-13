/**
 * ==============================================================================
 * ARCHIVO PRINCIPAL DE JAVASCRIPT (app.js)
 * ==============================================================================
 * Controla la interactividad ligera de la landing page (Vanilla ES6+).
 * Sin frameworks pesados para mantener máximo rendimiento y 0 overhead.
 */

document.addEventListener('DOMContentLoaded', () => {
    /**
     * --------------------------------------------------------------------------
     * 1. ANIMACIONES DE SCROLL (Intersection Observer)
     * --------------------------------------------------------------------------
     */
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                obs.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

    /**
     * --------------------------------------------------------------------------
     * 2. DESPLAZAMIENTO SUAVE (Smooth Scrolling)
     * --------------------------------------------------------------------------
     */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const currentHref = this.getAttribute('href');
            if (!currentHref || !currentHref.startsWith('#') || currentHref === '#') {
                return;
            }

            e.preventDefault();

            try {
                const target = document.querySelector(currentHref);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            } catch (err) {
                console.warn('Smooth scroll failed for:', currentHref);
            }
        });
    });

    /**
     * --------------------------------------------------------------------------
     * 3. GESTOR DE ENLACES DINÁMICOS (Data Links — usado en 404.html)
     * --------------------------------------------------------------------------
     */
    const CONTACT_LINKS = {
        linkedin: 'https://linkedin.com/in/sandra-puerto',
        github: 'https://github.com/sandra-puerto',
        email: 'mailto:contacto@sandrapuerto.com'
    };

    document.querySelectorAll('[data-link]').forEach(el => {
        const key = el.getAttribute('data-link');
        if (CONTACT_LINKS[key]) {
            el.setAttribute('href', CONTACT_LINKS[key]);
            if (CONTACT_LINKS[key].startsWith('http')) {
                el.setAttribute('target', '_blank');
                el.setAttribute('rel', 'noopener noreferrer');
            }
        }
    });
});
