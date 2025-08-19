// Hamburger menu toggle
// (shared for all pages)
document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.querySelector('.nav-toggle');
  const navCenter = document.querySelector('.nav-center');
  
  if (navToggle && navCenter) {
    navToggle.addEventListener('click', function() {
      navCenter.classList.toggle('open');
      navToggle.classList.toggle('open');
    });
    
    // Close menu when clicking on a link
    const navLinks = navCenter.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        navCenter.classList.remove('open');
        navToggle.classList.remove('open');
      });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navCenter.contains(e.target) && !navToggle.contains(e.target)) {
        navCenter.classList.remove('open');
        navToggle.classList.remove('open');
      }
    });
  }
});