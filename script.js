// Generate starfield
(function () {
  const container = document.getElementById('stars');
  if (!container) return;
  const count = 200;
  for (let i = 0; i < count; i++) {
    const star = document.createElement('div');
    const size = Math.random() * 2 + 0.5;
    const opacity = Math.random() * 0.6 + 0.1;
    Object.assign(star.style, {
      position: 'absolute',
      borderRadius: '50%',
      background: 'white',
      width: size + 'px',
      height: size + 'px',
      top: Math.random() * 100 + '%',
      left: Math.random() * 100 + '%',
      opacity: opacity,
      animation: `twinkle ${2 + Math.random() * 4}s ease-in-out infinite`,
      animationDelay: Math.random() * 4 + 's',
    });
    container.appendChild(star);
  }

  const style = document.createElement('style');
  style.textContent = `
    @keyframes twinkle {
      0%, 100% { opacity: var(--op, 0.3); }
      50% { opacity: calc(var(--op, 0.3) * 0.3); }
    }
  `;
  document.head.appendChild(style);
})();

// Smooth nav highlight on scroll
(function () {
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      nav.style.borderBottomColor = 'rgba(255,255,255,0.08)';
    } else {
      nav.style.borderBottomColor = 'rgba(255,255,255,0.07)';
    }
  }, { passive: true });
})();

// Fade-in on scroll
(function () {
  const els = document.querySelectorAll('.feature-card, .trust-card, .testimonial-card, .pricing-card, .press-card, .pro-card');
  const style = document.createElement('style');
  style.textContent = `
    .fade-up { opacity: 0; transform: translateY(24px); transition: opacity 0.5s ease, transform 0.5s ease; }
    .fade-up.visible { opacity: 1; transform: none; }
  `;
  document.head.appendChild(style);

  els.forEach((el, i) => {
    el.classList.add('fade-up');
    el.style.transitionDelay = (i % 4) * 80 + 'ms';
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.1 });

  els.forEach(el => observer.observe(el));
})();
