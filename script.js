// ========================================
// GALLERY MODAL FUNCTIONS
// ========================================
function openGalleryModal() {
    const modal = document.getElementById('galleryModal');
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeGalleryModal() {
    const modal = document.getElementById('galleryModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========================================
// MARKET CAMPAIGN MODAL FUNCTIONS
// ========================================
function openMarketCampaignModal() {
    console.log('Opening Market Campaign Modal...');
    const modal = document.getElementById('marketCampaignModal');
    console.log('Modal element:', modal);
    if (modal) {
        modal.style.display = 'block';
        modal.style.zIndex = '10000';
        document.body.style.overflow = 'hidden';
        console.log('Modal opened successfully!');
    } else {
        console.error('Modal not found!');
    }
}

function closeMarketCampaignModal() {
    console.log('Closing Market Campaign Modal...');
    const modal = document.getElementById('marketCampaignModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Image Lightbox Functionality
function openImageLightbox(src, alt) {
    // Prevent event from closing the modal
    event.stopPropagation();
    
    const lightbox = document.createElement('div');
    lightbox.className = 'image-lightbox';
    lightbox.innerHTML = `
        <span class="lightbox-close">&times;</span>
        <img src="${src}" alt="${alt}">
    `;
    
    document.body.appendChild(lightbox);
    
    // Close on clicking anywhere or close button
    lightbox.addEventListener('click', () => {
        lightbox.remove();
        document.body.style.overflow = 'hidden'; // Keep modal scroll disabled
    });
    
    // Close on Escape key
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            lightbox.remove();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

// ========================================
// MOBILE NAVIGATION
// ========================================
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}

document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    if (hamburger && navMenu) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
}));

// ========================================
// SMOOTH SCROLLING
// ========================================
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

// ========================================
// NAVBAR EFFECTS
// ========================================
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.classList.remove('scrolled');
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    }
});

// ========================================
// FIX FOR VISIBILITY - ENSURE CONTENT SHOWS
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // Make sure all content is visible first
    const ensureVisible = [
        '.timeline-item',
        '.timeline-content',
        '.skill-category',
        '.skill-items',
        '.project-card',
        '.about-content',
        '.about-text',
        '.about-skills'
    ];
    
    ensureVisible.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            // Remove any opacity: 0 that might be set
            el.style.opacity = '1';
            el.style.visibility = 'visible';
        });
    });
});

// ========================================
// INTERSECTION OBSERVER FOR ANIMATIONS (SIMPLIFIED)
// ========================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Add animation class but ensure visibility
            entry.target.style.opacity = '1';
            entry.target.classList.add('fade-in-up');
            entry.target.classList.add('animated');
        }
    });
}, observerOptions);

// ========================================
// SKILL BARS ANIMATION (FIXED)
// ========================================
const animateSkillBars = () => {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    skillBars.forEach(bar => {
        const barTop = bar.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (barTop < windowHeight - 50) {
            // Get width from style attribute or default
            const targetWidth = bar.style.width || '85%';
            
            // Only animate if not already animated
            if (!bar.classList.contains('animated')) {
                // Set width directly without hiding first
                bar.style.width = targetWidth;
                bar.classList.add('animated');
            }
        }
    });
};

// ========================================
// TYPING EFFECT FOR HERO SECTION (OPTIONAL)
// ========================================
class TypeWriter {
    constructor(element, words, wait = 3000) {
        this.element = element;
        this.words = words;
        this.wait = parseInt(wait, 10);
        this.txt = '';
        this.wordIndex = 0;
        this.isDeleting = false;
        this.type();
    }

    type() {
        const current = this.wordIndex % this.words.length;
        const fullTxt = this.words[current];

        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.element.innerHTML = `<span class="typing-text">${this.txt}</span>`;

        let typeSpeed = 100;

        if (this.isDeleting) {
            typeSpeed /= 2;
        }

        if (!this.isDeleting && this.txt === fullTxt) {
            typeSpeed = this.wait;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.wordIndex++;
            typeSpeed = 500;
        }

        setTimeout(() => this.type(), typeSpeed);
    }
}

// ========================================
// CONTACT FORM HANDLING
// ========================================
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const name = formData.get('name');
        const email = formData.get('email');
        const subject = formData.get('subject');
        const message = formData.get('message');
        
        if (!name || !email || !subject || !message) {
            showNotification('Please fill in all fields', 'error');
            return;
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }
        
        showNotification('Thank you for your message! I\'ll get back to you soon.', 'success');
        this.reset();
    });
}

// ========================================
// NOTIFICATION SYSTEM
// ========================================
function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// ========================================
// PARALLAX EFFECT (OPTIONAL - DISABLE IF CAUSING ISSUES)
// ========================================
// Commented out to prevent layout issues
/*
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    }
});
*/

// ========================================
// ACTIVE NAVIGATION HIGHLIGHTING
// ========================================
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ========================================
// COUNTER ANIMATION FOR STATS
// ========================================
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const isDecimal = target % 1 !== 0;
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = isDecimal ? start.toFixed(1) : Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = isDecimal ? target.toFixed(1) : target;
        }
    }
    
    updateCounter();
}

// ========================================
// INITIALIZE ON DOM CONTENT LOADED
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // CRITICAL: Ensure all content is visible
    const allContent = document.querySelectorAll('*');
    allContent.forEach(el => {
        if (el.style.opacity === '0') {
            el.style.opacity = '1';
        }
    });
    
    // Initialize animations only on elements that exist
    const animateElements = document.querySelectorAll('.timeline-item, .project-card, .skill-category');
    animateElements.forEach(el => {
        // Make sure element is visible before observing
        el.style.opacity = '1';
        observer.observe(el);
    });
    
    // Initialize gallery images
    const galleryImages = document.querySelectorAll('.modal-gallery-item img');
    galleryImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', (e) => {
            e.stopPropagation();
            openImageLightbox(img.src, img.alt);
        });
    });
    
    // Initialize counters
    const counters = document.querySelectorAll('.stat-number');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                const counter = entry.target;
                const target = parseFloat(counter.getAttribute('data-target') || counter.textContent);
                animateCounter(counter, target);
                counter.classList.add('counted');
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => counterObserver.observe(counter));
    
    // Initialize typing effect only if element exists
    const typingElement = document.querySelector('.typing-effect');
    if (typingElement) {
        const words = [
            'Data Analytics Engineer',
            'Business Intelligence Expert',
            'Cloud Solutions Architect',
            'Machine Learning Enthusiast'
        ];
        new TypeWriter(typingElement, words);
    }
    
    // Initialize project card hover effects
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click handler for Market Campaign card
    const marketCampaignCard = document.querySelector('.market-campaign-card');
    console.log('Market Campaign Card found:', marketCampaignCard);
    if (marketCampaignCard) {
        marketCampaignCard.addEventListener('click', function(e) {
            console.log('Market Campaign Card clicked!');
            e.preventDefault();
            e.stopPropagation();
            openMarketCampaignModal();
        });
        console.log('Click handler added to Market Campaign card');
    } else {
        console.error('Market Campaign card not found!');
    }
    
    // Animate skill bars after a short delay
    setTimeout(() => {
        animateSkillBars();
    }, 500);
});

// ========================================
// ADDITIONAL SCROLL LISTENERS
// ========================================
window.addEventListener('scroll', () => {
    animateSkillBars();
});

window.addEventListener('load', () => {
    // Final check to ensure everything is visible
    document.querySelectorAll('.timeline-item, .timeline-content, .skill-category, .project-card').forEach(el => {
        el.style.opacity = '1';
        el.style.visibility = 'visible';
    });
    
    // Animate skill bars on load
    animateSkillBars();
});

// ========================================
// MODAL CONTROLS
// ========================================
window.onclick = function(event) {
    const galleryModal = document.getElementById('galleryModal');
    const marketModal = document.getElementById('marketCampaignModal');
    
    if (event.target == galleryModal) {
        closeGalleryModal();
    }
    if (event.target == marketModal) {
        closeMarketCampaignModal();
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeGalleryModal();
        closeMarketCampaignModal();
    }
});

// ========================================
// EXPORT FUNCTIONS
// ========================================
window.openGalleryModal = openGalleryModal;
window.closeGalleryModal = closeGalleryModal;
window.openMarketCampaignModal = openMarketCampaignModal;
window.closeMarketCampaignModal = closeMarketCampaignModal;
window.openImageLightbox = openImageLightbox;
window.showNotification = showNotification;

// ========================================
// FAILSAFE: Force all content visible after 1 second
// ========================================
setTimeout(() => {
    document.querySelectorAll('*').forEach(el => {
        if (window.getComputedStyle(el).opacity === '0') {
            el.style.opacity = '1';
        }
        if (window.getComputedStyle(el).visibility === 'hidden') {
            el.style.visibility = 'visible';
        }
    });
}, 1000);