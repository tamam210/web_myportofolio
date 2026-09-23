import { useEffect, useRef, useState } from 'react';

const roles = ['Full-Stack Developer', 'Web Developer', 'Machine Learning Developer'];

function useTypewriter(words, { typeSpeed = 75, deleteSpeed = 40, pause = 1800 } = {}) {
  const [index, setIndex] = useState(0);
  const [text, setText] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = words[index % words.length];
    let timer;

    if (!deleting && text === current) {
      timer = setTimeout(() => setDeleting(true), pause);
    } else if (deleting && text === '') {
      setDeleting(false);
      setIndex((i) => (i + 1) % words.length);
    } else {
      timer = setTimeout(
        () => setText(current.slice(0, text.length + (deleting ? -1 : 1))),
        deleting ? deleteSpeed : typeSpeed
      );
    }

    return () => clearTimeout(timer);
  }, [words, text, deleting, index, typeSpeed, deleteSpeed, pause]);

  return text;
}

export default function Hero() {
  const typed = useTypewriter(roles);
  const heroRef = useRef(null);

  useEffect(() => {
    const hero = heroRef.current;
    if (!hero) return;

    const layers = Array.from(hero.querySelectorAll('.parallax'));
    let frame = 0;

    const onMouseMove = (e) => {
      const rect = hero.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;

      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        layers.forEach((el) => {
          const depth = parseFloat(el.dataset.depth) || 10;
          el.style.transform = `translate(${x * depth}px, ${y * depth}px)`;
        });
      });
    };

    hero.addEventListener('mousemove', onMouseMove);
    return () => {
      hero.removeEventListener('mousemove', onMouseMove);
      cancelAnimationFrame(frame);
    };
  }, []);

  return (
    <header id="home" className="hero" ref={heroRef}>
      <div className="hero-content">
        <p className="hero-greeting">Hi, my name is</p>
        <h1> Tamam Ni'amillah Ramdhan Putra Widyana 👋</h1>
        <h2 className="hero-subtitle">
          {typed}
          <span className="typewriter-cursor" aria-hidden="true"></span>
        </h2>
        <p>
          "Full-Stack Developer crafting FastAPI-powered backends, MySQL databases, Dockerized deployments, and intuitive web interfaces."
        </p>
        <div className="hero-actions">
          <a href="#projects" className="btn btn-primary">
            View My Projects
          </a>
          <a href="#contact" className="btn btn-outline">
            Get In Touch
          </a>
        </div>
      </div>
      <div className="hero-floats" aria-hidden="true">
        <span className="float-orb orb-1"></span>
        <span className="float-orb orb-2"></span>
        <span className="float-orb orb-3"></span>
        <span className="float-orb orb-4"></span>
        <span className="float-ring ring-1"></span>
        <span className="float-ring ring-2"></span>
        <span className="parallax pd-1" data-depth="18">
          <span className="float-dot fd-1"></span>
        </span>
        <span className="parallax pd-2" data-depth="26">
          <span className="float-dot fd-2"></span>
        </span>
        <span className="parallax pd-3" data-depth="14">
          <span className="float-dot fd-3"></span>
        </span>
        <span className="parallax pd-4" data-depth="32">
          <span className="float-dot fd-4"></span>
        </span>
        <span className="parallax pd-5" data-depth="22">
          <span className="float-dot fd-5"></span>
        </span>
      </div>
      <a href="#about" className="scroll-indicator" aria-label="Scroll down">
        <span className="scroll-mouse">
          <span className="scroll-wheel"></span>
        </span>
      </a>
    </header>
  );
}