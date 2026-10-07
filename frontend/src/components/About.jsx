import Reveal from './Reveal.jsx';
import profilePhoto from '../assets/profile.jpg';

const info = [
  { label: 'Degree', value: 'Informatics Engineering' },
  { label: 'Semester', value: '-----' },
  { label: 'Focus', value: 'Web & Macine learning (AI) Development' },
  { label: 'Status', value: 'Open to internships' },
];

export default function About() {
  return (
    <section id="about" className="about-section">
      <Reveal as="header" className="section-header">
        <h2>About Me</h2>
        <span className="underline" aria-hidden="true"></span>
      </Reveal>
      <Reveal delay={150} variant="up">
        <div className="about-content">
          <div className="about-photo">
            <img
              src={profilePhoto}
              alt="Foto Tamam Ni'amillah Ramdhan Putra Widyana"
              loading="lazy"
            />
          </div>
          <div className="about-text">
            <p>
              "I'm a Full-Stack Developer specializing in building robust backends with MySQL,
              containerized deployments using Docker, and clean, responsive web interfaces.
              I enjoy turning complex ideas into scalable, efficient, and user-friendly digital solutions.
            </p>
            <p>
              Every project I build sharpens my engineering skills and brings scalable solutions to life.
              I’m ready to collaborate, tackle complex technical challenges, and drive real value in the software industry."
            </p>
            <ul className="about-info">
              {info.map((item) => (
                <li key={item.label}>
                  <strong>{item.label}:</strong> {item.value}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Reveal>
    </section>
  );
}
