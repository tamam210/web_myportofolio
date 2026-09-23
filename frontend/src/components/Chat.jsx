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

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const sessionId = useRef(getSessionId());
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const send = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text }]);
    setLoading(true);

    try {
      const { data } = await axios.post('/api/chat', {
        message: text,
        session_id: sessionId.current,
      });
      setMessages((prev) => [...prev, { role: 'bot', text: data.reply, askEmail: data.ask_email }]);
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
            <div className="chat-message bot">
              Halo! 👋 Aku bot dari portfolio Tamam. Tanya-tanya soal skill, project, atau kontak, atau ketik apa aja yang kamu mau tanya.
            </div>
            {messages.map((msg, i) => (
              <div key={i} className={`chat-message ${msg.role}`}>
                {msg.text}
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