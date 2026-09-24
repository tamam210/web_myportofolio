import { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import Reveal from './Reveal.jsx';

function getSessionId() {
  let id = localStorage.getItem('chat_session');
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem('chat_session', id);
  }
  return id;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const GREETING =
  "Halo! 👋 Aku bot dari portfolio Tamam. Tanya-tanya soal skill, project, atau kontak, " +
  "atau ketik apa aja yang kamu mau tanya.\n\n" +
  "**Jika jawaban anda belum dijawab atau belum sesuai dengan pertanyaan anda mohon tulis/prompt** " +
  '***tolong tanyakan kepada developer anda "pertanyaan"***';

function renderInline(text) {
  const nodes = [];
  const tokens = String(text).split(/(\*\*\*.*?\*\*\*)/g);
  tokens.forEach((tok, ti) => {
    if (tok.startsWith('***') && tok.endsWith('***') && tok.length > 6) {
      nodes.push(
        <em key={ti}>
          <strong>{tok.slice(3, -3)}</strong>
        </em>
      );
      return;
    }
    const subs = tok.split(/(\*\*.*?\*\*)/g);
    subs.forEach((sub, si) => {
      if (sub.startsWith('**') && sub.endsWith('**') && sub.length > 4) {
        nodes.push(<strong key={`${ti}-${si}`}>{sub.slice(2, -2)}</strong>);
        return;
      }
      const its = sub.split(/(\*.*?\*)/g);
      its.forEach((it, ii) => {
        if (it.startsWith('*') && it.endsWith('*') && it.length > 2) {
          nodes.push(<em key={`${ti}-${si}-${ii}`}>{it.slice(1, -1)}</em>);
          return;
        }
        it.split('\n').forEach((line, li) => {
          if (li > 0) nodes.push(<br key={`br-${ti}-${si}-${ii}-${li}`} />);
          if (line) nodes.push(line);
        });
      });
    });
  });
  return nodes;
}

export default function Chat() {
  const [messages, setMessages] = useState([{ role: 'bot', text: GREETING }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showEmailModal, setShowEmailModal] = useState(true);
  const [userEmail, setUserEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const sessionId = useRef(getSessionId());
  const chatBoxRef = useRef(null);
  const emailModalRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, loading]);

  useEffect(() => {
    const overlay = emailModalRef.current;
    const visualViewport = window.visualViewport;
    if (!overlay || !visualViewport) return;

    const updateViewport = () => {
      overlay.style.setProperty('--visual-viewport-height', `${visualViewport.height}px`);
    };

    updateViewport();
    visualViewport.addEventListener('resize', updateViewport);

    return () => {
      visualViewport.removeEventListener('resize', updateViewport);
    };
  }, [showEmailModal]);

  const emailValid = EMAIL_RE.test(userEmail.trim());

  const startChat = (e) => {
    e.preventDefault();
    if (!emailValid) {
      setEmailError('Email-nya kayaknya belum bener. Contoh: nama@email.com');
      return;
    }
    setEmailError('');
    setShowEmailModal(false);
  };

  const send = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading || !emailValid) return;

    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text }]);
    setLoading(true);

    try {
      const { data } = await axios.post('/api/chat', {
        message: text,
        session_id: sessionId.current,
        user_email: userEmail.trim(),
      });
      setMessages((prev) => [...prev, { role: 'bot', text: data.reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'bot', text: 'Ups, server-nya lagi tidur 😴 Coba lagi nanti ya!' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="contact" className="chat-section">
      {showEmailModal && (
        <div className="email-modal-overlay" ref={emailModalRef}>
          <div className="email-modal">
            <form onSubmit={startChat}>
              <div className="email-modal-content">
                <h3>Mulai Ngobrol 💬</h3>
                <p>
                  Kasih alamat email dulu ya — kalau ada pertanyaan yang belum bisa ku-jawab,
                  jawabannya bakal kukirim ke email kamu. 🙏
                </p>
                <input
                  type="email"
                  value={userEmail}
                  onChange={(e) => {
                    setUserEmail(e.target.value);
                    setEmailError('');
                  }}
                  placeholder="nama@email.com"
                />
                {emailError && <span className="email-modal-error">{emailError}</span>}
              </div>
              <button type="submit" className="btn btn-primary">
                Mulai Chat 🚀
              </button>
            </form>
          </div>
        </div>
      )}

      <Reveal>
        <div className="section-header">
          <h2>Chat With Me</h2>
          <div className="underline"></div>
        </div>
      </Reveal>
      <Reveal delay={120}>
        <div className="chat-card">
          <div className="chat-header">
            <span className="chat-status-dot"></span>
            <strong>GW Portfolio Bot</strong>
            <span className="chat-status">online</span>
          </div>

          <div className="chat-box" ref={chatBoxRef}>
            {messages.map((msg, i) => (
              <div key={i} className={`chat-message ${msg.role}`}>
                {renderInline(msg.text)}
              </div>
            ))}
            {loading && (
              <div className="chat-message bot">
                <span className="chat-typing">
                  <span></span><span></span><span></span>
                </span>
              </div>
            )}
          </div>

          <form className="chat-form" onSubmit={send}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ketik pesan kamu..."
              disabled={loading}
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              Kirim
            </button>
          </form>
        </div>
      </Reveal>
    </section>
  );
}