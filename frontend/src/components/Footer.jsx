import Reveal from './Reveal.jsx';

const socialLinks = [
  {
    label: 'GitHub',
    href: 'https://github.com/tamam210',
    icon: 'github',
    external: true,
  },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/tamam-niam-958518423/',
    icon: 'linkedin',
    external: true,
  },
  {
    label: 'Email',
    href: 'mailto:tamam.niamillah.rpw@gmail.com',
    icon: 'email',
    external: false,
  },
];

function SocialIcon({ type }) {
  if (type === 'github') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M12 .5C5.73.5.5 5.73.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56v-2.17c-3.2.7-3.88-1.37-3.88-1.37-.52-1.34-1.27-1.7-1.27-1.7-1.04-.71.08-.7.08-.7 1.15.08 1.75 1.18 1.75 1.18 1.02 1.75 2.67 1.25 3.32.96.1-.75.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.68 0-1.25.45-2.27 1.18-3.07-.12-.29-.51-1.45.11-3.03 0 0 .96-.31 3.15 1.17a10.9 10.9 0 0 1 5.76 0c2.19-1.48 3.15-1.17 3.15-1.17.62 1.58.23 2.74.11 3.03.73.8 1.18 1.82 1.18 3.07 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.68.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.73 18.27.5 12 .5Z" />
      </svg>
    );
  }

  if (type === 'linkedin') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M5.33 3.33a2.33 2.33 0 1 1 0 4.66 2.33 2.33 0 0 1 0-4.66ZM3.2 9.5h4.3V21H3.2V9.5Zm7.3 0h4.12v1.57h.06c.57-1.08 1.96-2.22 4.04-2.22 4.32 0 5.12 2.84 5.12 6.54V21h-4.3v-5.06c0-1.21-.02-2.76-1.68-2.76-1.68 0-1.94 1.31-1.94 2.67V21h-4.3V9.5Z" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M3 5.5A2.5 2.5 0 0 1 5.5 3h13A2.5 2.5 0 0 1 21 5.5v13a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 18.5v-13Zm2.2-.5 6.8 5.4L18.8 5H5.2ZM19 6.8l-6.78 5.4a.8.8 0 0 1-.84 0L4.5 6.8v10.7c0 .28.22.5.5.5h14a.5.5 0 0 0 .5-.5V6.8Z" />
    </svg>
  );
}

export default function Footer() {
  return (
    <footer>
      <Reveal variant="up">
        <p>Built with passion by an Informatics Engineering student.</p>
        <nav className="footer-links" aria-label="Social and contact links">
          {socialLinks.map((link) => (
            <a
              key={link.label}
              className="social-link"
              href={link.href}
              target={link.external ? '_blank' : undefined}
              rel={link.external ? 'noopener noreferrer' : undefined}
              aria-label={link.label}
            >
              <SocialIcon type={link.icon} />
            </a>
          ))}
        </nav>
        <p className="copyright">&copy; {new Date().getFullYear()} MyPortfolio. All rights reserved.</p>
      </Reveal>
    </footer>
  );
}