/* ===================================
   PORTFOLIO JAVASCRIPT
   =================================== */

// Global config for external dashboards (update for Netlify)
const DASHBOARD_URL = (window.DASHBOARD_URL_OVERRIDE) || 'http://localhost:8001';

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Mobile navigation toggle
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Project Modal Functions
function openModal() {
    document.getElementById('projectModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('projectModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Flight Delay Modal Functions
function openFlightModal() {
    document.getElementById('flightModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeFlightModal() {
    document.getElementById('flightModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Image Lightbox Functions
function openImage(src) {
    event.stopPropagation();
    const lightbox = document.getElementById('imageLightbox');
    const lightboxImg = document.getElementById('lightboxImage');
    lightbox.style.display = 'block';
    lightboxImg.src = src;
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('imageLightbox').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
        closeFlightModal();
        closeLightbox();
    }
});

// Close modal on outside click
window.onclick = function(event) {
    const projectModal = document.getElementById('projectModal');
    const flightModal = document.getElementById('flightModal');
    
    if (event.target == projectModal) {
        closeModal();
    }
    if (event.target == flightModal) {
        closeFlightModal();
    }
}

// Contact form handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your message! I will get back to you soon.');
        this.reset();
    });
}

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.background = 'rgba(10, 14, 39, 0.98)';
        navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.7)';
    } else {
        navbar.style.background = 'rgba(10, 14, 39, 0.95)';
        navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.5)';
    }
    
    lastScroll = currentScroll;
});

// Animate skill bars on scroll
const observerOptions = {
    threshold: 0.5
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const skillFills = entry.target.querySelectorAll('.skill-fill');
            skillFills.forEach(fill => {
                fill.style.animation = 'skillFill 2s ease-out forwards';
            });
        }
    });
}, observerOptions);

const skillCards = document.querySelectorAll('.skill-card');
skillCards.forEach(card => observer.observe(card));

console.log('Portfolio loaded successfully! 🎉');

// Wire Flight Dashboard links to configurable URL
(() => {
    const link = document.getElementById('flight-dashboard-link');
    const btn = document.getElementById('flight-dashboard-open-btn');
    if (link) link.href = DASHBOARD_URL;
    if (btn) btn.href = DASHBOARD_URL;
})();
