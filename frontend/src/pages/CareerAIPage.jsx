import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api';
import { MessageSquare, Sparkles, Send, User, Bot, BookOpen, ChevronRight, Layers } from 'lucide-react';
import Badge from '../components/Badge';

const CareerAIPage = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I am **CareerAI**, your personal career intelligence advisor. I have real-time access to your verified skill profile, assessment scores, and career gap analysis. How can I help you accelerate your journey today?",
      sources: ["Student Profile", "Adaptive Assessment Bank", "Career Role Registry"],
      suggested_followups: [
        "What is my top recommended career?",
        "Show my critical skill gaps",
        "Suggest high-impact portfolio projects",
        "Give me a mock interview question"
      ]
    }
  ]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (messageText) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || sending) return;

    const userMsg = { role: 'user', content: textToSend };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setSending(true);

    try {
      const res = await api.post('/ai/chat', { message: textToSend });
      const botMsg = {
        role: 'assistant',
        content: res.data.reply,
        sources: res.data.sources_used || [],
        suggested_followups: res.data.suggested_followups || []
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (e) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "I encountered a network hiccup while retrieving your latest assessment records. Please try asking again.",
          sources: []
        }
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-8rem)]">
      
      {/* Header */}
      <div className="glass-card p-4 sm:p-5 flex items-center justify-between mb-4 shadow-sm shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-primary-600 to-indigo-500 text-white flex items-center justify-center font-bold shadow-md shadow-primary-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-base text-slate-900 dark:text-white">CareerAI Advisor</h1>
              <Badge variant="primary" className="text-[10px]">RAG Context Active</Badge>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">
              Personalized guidance with verified profile context
            </p>
          </div>
        </div>
      </div>

      {/* Chat Messages Log */}
      <div className="flex-1 glass-card p-4 sm:p-6 overflow-y-auto space-y-5">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-xs font-bold ${
              msg.role === 'user'
                ? 'bg-slate-800 text-white dark:bg-slate-200 dark:text-slate-900'
                : 'bg-primary-600 text-white shadow-sm shadow-primary-500/20'
            }`}>
              {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div className={`max-w-[85%] sm:max-w-[75%] space-y-2 ${msg.role === 'user' ? 'text-right' : ''}`}>
              <div className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed text-left ${
                msg.role === 'user'
                  ? 'bg-primary-600 text-white font-medium rounded-tr-none'
                  : 'bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-100 border border-slate-200/60 dark:border-slate-800 rounded-tl-none whitespace-pre-line'
              }`}>
                {msg.content}
              </div>

              {/* Sources */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5 text-[10px] text-slate-400 pt-1">
                  <span className="font-semibold">Context Sources:</span>
                  {msg.sources.map((src, sIdx) => (
                    <span key={sIdx} className="px-2 py-0.5 rounded-md bg-slate-200/60 dark:bg-slate-800/80 font-mono">
                      {src}
                    </span>
                  ))}
                </div>
              )}

              {/* Follow-up Prompt Chips */}
              {msg.suggested_followups && msg.suggested_followups.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-2">
                  {msg.suggested_followups.map((chip, cIdx) => (
                    <button
                      key={cIdx}
                      onClick={() => handleSend(chip)}
                      className="text-[11px] px-2.5 py-1 rounded-lg bg-primary-50 dark:bg-primary-950/60 text-primary-600 dark:text-primary-400 border border-primary-200/50 dark:border-primary-800/50 hover:bg-primary-100 font-medium transition-colors text-left flex items-center gap-1"
                    >
                      <span>{chip}</span>
                      <ChevronRight className="w-3 h-3 shrink-0" />
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {sending && (
          <div className="flex items-center gap-3 text-xs text-slate-400">
            <div className="w-8 h-8 rounded-xl bg-primary-600 text-white flex items-center justify-center font-bold">
              <Bot className="w-4 h-4 animate-pulse" />
            </div>
            <span>CareerAI is analyzing your profile telemetry...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="glass-card p-3 flex items-center gap-2 mt-3 shadow-md shrink-0"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about your skill gaps, recommendations, or projects..."
          className="flex-1 bg-transparent px-3 py-2 text-xs text-slate-900 dark:text-white outline-none placeholder:text-slate-400"
        />
        <button
          type="submit"
          disabled={!input.trim() || sending}
          className="px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 disabled:opacity-40 transition-all flex items-center gap-1.5"
        >
          <Send className="w-3.5 h-3.5" />
          <span>Send</span>
        </button>
      </form>

    </div>
  );
};

export default CareerAIPage;
