import Reveal from './Reveal.jsx';

const skills = [
  {
    icon: '🏗️',
    title: 'HTML',
    description: 'Semantic structure, accessibility, and best practices for clean markup.',
  },
  {
    icon: '🎨',
    title: 'CSS',
    description: 'Flexbox, Grid, responsive design, and modern styling techniques.',
  },
  {
    icon: '⚡',
    title: 'JavaScript',
    description: 'DOM manipulation, events, and interactive user experiences.',
  },
  {
    icon: '🛠️',
    title: 'Git & GitHub',
    description: 'Version control, branching, and collaborating on projects.',
  },
  {
    icon: '🐬',
    title: 'MySQL',
    description: 'Database design, SQL queries, and managing relational data.',
  },
  {
    icon: '🐍',
    title: 'Python',
    description: 'Scripting, automation, data handling, and building backend logic.',
  },
  {
    icon: '⚛️',
    title: 'React',
    description: 'Component-based UI development with hooks and modern SPA patterns.',
  },
  {
    icon: '🚀',
    title: 'FastAPI',
    description: 'Building fast, modern REST APIs with Python and automatic docs.',
  },
];

export default function Skills() {
  return (
    <section id="skills" className="skills-section">
      <Reveal>
        <div className="section-header">
          <h2>My Skills</h2>
          <div className="underline"></div>
        </div>
      </Reveal>
      <div className="skills-container">
        {skills.map((skill, i) => (
          <Reveal key={skill.title} delay={i * 90} variant="up">
            <article className="skill-card">
              <div className="skill-icon">{skill.icon}</div>
              <h3>{skill.title}</h3>
              <p>{skill.description}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </section>
  );
}