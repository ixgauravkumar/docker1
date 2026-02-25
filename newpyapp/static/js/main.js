/* =====================================================
   CIVILRAJ MODERN UI JS (2026 VERSION)
===================================================== */


/* ================= COUNTER ANIMATION ================= */

const counters = document.querySelectorAll(".counter");

if (counters.length > 0) {

    counters.forEach(counter => {

        const updateCounter = () => {

            const target = +counter.getAttribute("data-target");
            const count = +counter.innerText;

            const increment = target / 120;

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        };

        updateCounter();
    });
}


/* ================= SCROLL REVEAL ================= */

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });

}, {
    threshold: 0.15
});

document.querySelectorAll(".fade-in")
    .forEach(el => observer.observe(el));


/* ================= NAVBAR SCROLL EFFECT ================= */

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if (!navbar) return;

    if (window.scrollY > 40) {
        navbar.classList.add("nav-scrolled");
    } else {
        navbar.classList.remove("nav-scrolled");
    }
});


/* ================= HERO FADE LOAD ================= */

window.addEventListener("load", () => {

    const heroText = document.querySelector(".hero-text");

    if (heroText) {
        heroText.classList.add("hero-visible");
    }
});
