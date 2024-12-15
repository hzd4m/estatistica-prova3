// JavaScript para o tema espacial moderno

// Splash Screen
window.addEventListener('load', () => {
    const splashScreen = document.getElementById('splash-screen');
    setTimeout(() => {
        splashScreen.style.opacity = '0';
        setTimeout(() => splashScreen.style.display = 'none', 500);
    }, 3000); // Tempo da splash screen (3 segundos)
});

// Animação de partículas no fundo
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
document.body.appendChild(canvas);

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const particleCount = 100;

for (let i = 0; i < particleCount; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2,
        speedX: (Math.random() - 0.5) * 0.5,
        speedY: (Math.random() - 0.5) * 0.5
    });
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => {
        particle.x += particle.speedX;
        particle.y += particle.speedY;

        if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1;

        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();
    });

    requestAnimationFrame(animateParticles);
}

animateParticles();

// Interações dos botões
const buttons = document.querySelectorAll('.action-button');
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.left = `${event.offsetX}px`;
        ripple.style.top = `${event.offsetY}px`;
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});
