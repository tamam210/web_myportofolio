import Reveal from './Reveal.jsx';

const projects = [
  {
    title: 'App Blocker',
    tags: ['Flask', 'REST API', 'Python', 'Next.js', 'Tailwind CSS'],
    description:
      'Full-stack productivity tool that automatically blocks distracting apps on Windows. A Next.js frontend pairs with a Python Flask backend exposing a REST API to manage presets, custom schedules, and app lists.',
    demo: null,
    code: 'https://github.com/tamam210/apps.blocked',
    docs: 'https://github.com/tamam210/apps.blocked#readme',
  },
  {
    title: 'Sensory Platform',
    tags: ['Next.js', 'React', 'Tailwind CSS'],
    description:
      'Web platform project for the Sensory brand — initial repository setup and architecture foundation for a polished, responsive online presence.',
    demo: null,
    code: 'https://github.com/tamam210/sensory.id',
    docs: 'https://github.com/tamam210/sensory.id#readme',
  },
  {
    title: 'UTC Landing Page',
    tags: ['HTML', 'CSS', 'JavaScript'],
    description:
      'Responsive landing page for Unida Technologic Care promoting tech services. Features bilingual EN/ID toggling, service highlights, and a team section built with pure HTML, CSS, and JavaScript.',
    demo: null,
    code: 'https://github.com/tamam210/Project_UTC',
    docs: 'https://github.com/tamam210/Project_UTC#readme',
  },
];

export default function Projects() {
  return (
    <section id="projects" className="projects-section">
      <Reveal>
        <div className="section-header">
          <h2>Featured Projects</h2>
          <div className="underline"></div>
        </div>
      </Reveal>
      <div className="card-container">
        {projects.map((project, i) => (
          <Reveal key={project.title} delay={i * 120} variant="up">
            <article className="card">
              <div className="card-tags">
                {project.tags.map((tag) => (
                  <span className="card-tag" key={tag}>
                    {tag}
                  </span>
                ))}
              </div>
              <h3>{project.title}</h3>
              <p>{project.description}</p>
              <div className="card-links">
                <a href={project.code} target="_blank" rel="noopener">
                  View Code &rarr;
                </a>
                {project.demo && (
                  <a href={project.demo} target="_blank" rel="noopener">
                    Live Demo &rarr;
                  </a>
                )}
                <a href={project.docs} target="_blank" rel="noopener">
                  Docs
                </a>
              </div>
            </article>
          </Reveal>
        ))}
      </div>
    </section>
  );
}