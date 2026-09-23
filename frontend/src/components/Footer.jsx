import Reveal from './Reveal.jsx';

export default function Footer() {
  return (
    <footer>
      <Reveal variant="up">
        <p>Built with passion by an Informatics Engineering student.</p>
        <div className="footer-links">
          <a href="https://github.com" target="_blank" rel="noopener">GitHub</a>
          <a href="https://linkedin.com" target="_blank" rel="noopener">LinkedIn</a>
          <a href="mailto:tamam.niamillah.rpw@gmail.com">Email</a>
        </div>
        <p className="copyright">&copy; {new Date().getFullYear()} MyPortfolio. All rights reserved.</p>
      </Reveal>
    </footer>
  );
}