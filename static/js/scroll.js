    // Show/hide button on scroll
    window.onscroll = function() {
    const btn = document.getElementById("scrollToTopBtn");
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
    };

    // Scroll to top smoothly
    function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
    }