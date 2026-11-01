// Cabecera: borde al hacer scroll y menú móvil
const nav = document.querySelector('.nav');
const toggle = document.querySelector('.nav__toggle');

const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 10);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', open);
});
document.querySelectorAll('.nav__links a').forEach(a =>
  a.addEventListener('click', () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', false);
  })
);

// Aparición suave de elementos
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('is-visible');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Filtro de tipologías
const filters = document.querySelectorAll('.filter');
const projects = document.querySelectorAll('.project');
filters.forEach(btn => btn.addEventListener('click', () => {
  filters.forEach(b => b.classList.remove('is-active'));
  btn.classList.add('is-active');
  const f = btn.dataset.filter;
  projects.forEach(p => p.classList.toggle('is-hidden', f !== 'all' && p.dataset.cat !== f));
}));

// Formulario: abre el correo del usuario con la consulta rellenada
const form = document.getElementById('contact-form');
const status = form.querySelector('.form__status');
const EMAIL_ESTUDIO = 'info@enriquesanchezpolo.es'; // cambiar por el email real

form.addEventListener('submit', e => {
  e.preventDefault();
  if (!form.checkValidity()) {
    status.textContent = 'Por favor, completa los campos obligatorios y acepta la política de privacidad.';
    return;
  }
  const d = new FormData(form);
  const subject = `Consulta web: ${d.get('servicio')}`;
  const body = `Nombre: ${d.get('nombre')}\nTeléfono: ${d.get('telefono')}\nEmail: ${d.get('email')}\nServicio: ${d.get('servicio')}\n\n${d.get('mensaje')}`;
  window.location.href = `mailto:${EMAIL_ESTUDIO}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  status.textContent = 'Gracias. Se abrirá tu programa de correo para enviar la consulta.';
});

document.getElementById('year').textContent = new Date().getFullYear();
