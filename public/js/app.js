/**
 * ==============================================================================
 * ARCHIVO PRINCIPAL DE JAVASCRIPT (app.js)
 * ==============================================================================
 * Este archivo controla la interactividad de la landing page.
 * Est├í dise├▒ado para ser ligero, modular y f├ícil de entender.
 * 
 * ┬┐Por qu├® usamos Vanilla JS en lugar de React/Vue?
 * Para una landing page est├ítica, los frameworks pesados a├▒aden tiempo de carga
 * innecesario. Vanilla JS nos permite alcanzar 100/100 en Google Lighthouse.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    /**
     * --------------------------------------------------------------------------
     * 1. ANIMACIONES DE SCROLL (Intersection Observer)
     * --------------------------------------------------------------------------
     * Problema: Queremos que los elementos aparezcan suavemente a medida que el 
     * usuario hace scroll hacia abajo.
     * 
     * Soluci├│n: Usamos IntersectionObserver, una API nativa del navegador que es
     * mucho m├ís eficiente que escuchar el evento 'scroll' (lo cual ralentiza la p├ígina).
     */
    const observerOptions = {
        root: null,           // Usa el viewport (la ventana del navegador) como ├írea de visi├│n.
        rootMargin: '0px',    // Margen antes de activar (0px significa exactamente al entrar).
        threshold: 0.15       // El elemento debe ser 15% visible antes de disparar la animaci├│n.
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // Si el elemento entra en la pantalla...
            if (entry.isIntersecting) {
                // A├▒adimos la clase '.visible' que dispara la transici├│n CSS (opacity 0 -> 1)
                entry.target.classList.add('visible');
                
                // OPTIMIZACI├ôN: Una vez que el elemento ya apareci├│, dejamos de observarlo.
                // Esto libera memoria y CPU, mejorando el rendimiento global.
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Seleccionamos todos los elementos con '.fade-up' (excepto el Hero, que usa CSS puro por LCP)
    const fadeElements = document.querySelectorAll('.fade-up');
    fadeElements.forEach(el => observer.observe(el));


    /**
     * --------------------------------------------------------------------------
     * 2. L├ôGICA DEL ACORDE├ôN (FAQ)
     * --------------------------------------------------------------------------
     * Este script maneja la apertura y cierre de las preguntas frecuentes.
     * Solo permite que un elemento est├® abierto a la vez para mantener la limpieza visual.
     */
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // 2.1. Primero, cerramos todos los dem├ís elementos que est├®n abiertos.
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // 2.2. Luego, alternamos (abrir/cerrar) el elemento que el usuario clic├│.
            // La clase '.active' expande el contenedor v├¡a CSS (max-height).
            item.classList.toggle('active');
        });
    });


    /**
     * --------------------------------------------------------------------------
     * 3. DESPLAZAMIENTO SUAVE (Smooth Scrolling)
     * --------------------------------------------------------------------------
     * Cuando un usuario hace clic en un enlace de navegaci├│n interno (ej. #servicios),
     * hacemos que la p├ígina baje suavemente en lugar de saltar bruscamente.
     */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const currentHref = this.getAttribute('href');
            
            // Si el enlace es inyectado, vac├¡o o solo '#', ignoramos para no causar errores.
            if (!currentHref.startsWith('#') || currentHref === '#') {
                return;
            }

            e.preventDefault(); // Previene el salto predeterminado del navegador
            
            try {
                const target = document.querySelector(currentHref);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start' // Alinea el elemento al principio de la pantalla
                    });
                }
            } catch (err) {
                console.warn("Smooth scroll failed for: ", currentHref);
            }
        });
    });


    /**
     * --------------------------------------------------------------------------
     * 4. GESTOR DE ENLACES DIN├üMICOS (Data Links)
     * --------------------------------------------------------------------------
     * Problema: Si cambiamos el correo o el link de LinkedIn, tendr├¡amos que buscar
     * en todo el HTML para reemplazarlo.
     * 
     * Soluci├│n: Centralizamos los enlaces aqu├¡. En el HTML usamos atributos
     * personalizados como: data-link="email", y este script se encarga de inyectar el href.
     */
    const CONTACT_LINKS = {
        linkedin: "https://linkedin.com/in/sandra-puerto",
        email: "mailto:contacto@sandrapuerto.com",
        calendar: "https://calendar.app.google/H3i9G1zKtFZY7krd6",
        stratum: "https://github.com/sandra-puerto/stratum-core"
    };

    // Buscamos todos los elementos en el HTML que tengan el atributo 'data-link'
    document.querySelectorAll('[data-link]').forEach(el => {
        const key = el.getAttribute('data-link'); // ej: 'email' o 'linkedin'
        
        if (CONTACT_LINKS[key]) {
            // Le inyectamos el enlace real al atributo href
            el.setAttribute('href', CONTACT_LINKS[key]);
            
            // Buena Pr├íctica de Seguridad: Si es un link externo, a├▒adimos rel="noopener"
            if (CONTACT_LINKS[key].startsWith('http')) {
                el.setAttribute('target', '_blank'); // Abrir en nueva pesta├▒a
                el.setAttribute('rel', 'noopener noreferrer'); // Previene ataques Reverse Tabnabbing
            }
        }
    });
});
