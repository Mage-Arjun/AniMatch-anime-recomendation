// Sticky Navbar with Scroll Effects
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (window.innerWidth > 1024) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    } else {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled-mobile');
        } else {
            navbar.classList.remove('scrolled-mobile');
        }
    }
});
// Mobile Menu Toggle
function toggleMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.querySelector('.overlay');
    
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    overlay.classList.toggle('active');
    
    // Prevent body scroll when menu is open
    document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : 'auto';
}

function closeMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.querySelector('.overlay');
    
    hamburger.classList.remove('active');
    mobileMenu.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Page Navigation Handler (example: for single page app)
function showPage(pageId) {
    // Assume this function is implemented to switch pages
    // Here you just update active nav link states
    
    // Update desktop nav active
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    if (event && event.target) event.target.classList.add('active');
    
    // Update mobile nav active
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    mobileNavLinks.forEach(link => link.classList.remove('active'));
    const mobileLink = document.querySelector(`.mobile-nav-link[onclick="showPage('${pageId}')"]`);
    if (mobileLink) mobileLink.classList.add('active');
    
    // Close mobile menu if open
    closeMobileMenu();
    
    // Scroll to top or show page logic should be here
    window.scrollTo(0, 0);
}
