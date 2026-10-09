/**
 * ==============================================================================
 * ARCHIVO PRINCIPAL DE JAVASCRIPT (app.js)
 * ==============================================================================
 * Este archivo controla la interactividad de la landing page.
 * Está diseñado para ser ligero, modular y fácil de entender.
 * 
 * ¿Por qué usamos Vanilla JS en lugar de React/Vue?
 * Para una landing page estática, los frameworks pesados añaden tiempo de carga
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
     * Solución: Usamos IntersectionObserver, una API nativa del navegador que es
     * mucho más eficiente que escuchar el evento 'scroll' (lo cual ralentiza la página).
     */
    const observerOptions = {
        root: null,           // Usa el viewport (la ventana del navegador) como área de visión.
        rootMargin: '0px',    // Margen antes de activar (0px significa exactamente al entrar).
        threshold: 0.15       // El elemento debe ser 15% visible antes de disparar la animación.
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // Si el elemento entra en la pantalla...
            if (entry.isIntersecting) {
                // Añadimos la clase '.visible' que dispara la transición CSS (opacity 0 -> 1)
                entry.target.classList.add('visible');
                
                // OPTIMIZACIÓN: Una vez que el elemento ya apareció, dejamos de observarlo.
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
     * 2. LÓGICA DEL ACORDEÓN (FAQ)
     * --------------------------------------------------------------------------
     * Este script maneja la apertura y cierre de las preguntas frecuentes.
     * Solo permite que un elemento esté abierto a la vez para mantener la limpieza visual.
     */
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // 2.1. Primero, cerramos todos los demás elementos que estén abiertos.
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // 2.2. Luego, alternamos (abrir/cerrar) el elemento que el usuario clicó.
            // La clase '.active' expande el contenedor vía CSS (max-height).
            item.classList.toggle('active');
        });
    });


    /**
     * --------------------------------------------------------------------------
     * 3. DESPLAZAMIENTO SUAVE (Smooth Scrolling)
     * --------------------------------------------------------------------------
     * Cuando un usuario hace clic en un enlace de navegación interno (ej. #servicios),
     * hacemos que la página baje suavemente en lugar de saltar bruscamente.
     */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const currentHref = this.getAttribute('href');
            
            // Si el enlace es inyectado, vacío o solo '#', ignoramos para no causar errores.
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
     * 4. GESTOR DE ENLACES DINÁMICOS (Data Links)
     * --------------------------------------------------------------------------
     * Problema: Si cambiamos el correo o el link de LinkedIn, tendríamos que buscar
     * en todo el HTML para reemplazarlo.
     * 
     * Solución: Centralizamos los enlaces aquí. En el HTML usamos atributos
     * personalizados como: data-link="email", y este script se encarga de inyectar el href.
     */
    const CONTACT_LINKS = {
        linkedin: "https://linkedin.com/in/sandra-puerto",
        email: "mailto:contacto@sandrapuerto.com",
        calendar: "https://calendar.app.google/H3i9G1zKtFZY7krd6",
        stratum: "https://github.com/sandra-puerto/stratum"
    };

    // Buscamos todos los elementos en el HTML que tengan el atributo 'data-link'
    document.querySelectorAll('[data-link]').forEach(el => {
        const key = el.getAttribute('data-link'); // ej: 'email' o 'linkedin'
        
        if (CONTACT_LINKS[key]) {
            // Le inyectamos el enlace real al atributo href
            el.setAttribute('href', CONTACT_LINKS[key]);
            
            // Buena Práctica de Seguridad: Si es un link externo, añadimos rel="noopener"
            if (CONTACT_LINKS[key].startsWith('http')) {
                el.setAttribute('target', '_blank'); // Abrir en nueva pestaña
                el.setAttribute('rel', 'noopener noreferrer'); // Previene ataques Reverse Tabnabbing
            }
        }
    });
});