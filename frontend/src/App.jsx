import { useState, useEffect } from 'react'
import UploadForm from './components/UploadForm.jsx'
import './App.css'

export default function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(t => (t === 'dark' ? 'light' : 'dark'))
  }
    return (
        <div className="app-shell">
            {/* ── Nav ─────────────────────────────────────────────────── */}
            <header className="nav">
                <div className="nav-inner">
                    <div className="nav-logo">
                        <span className="logo-dot" aria-hidden="true" />
                        <span>Rabbitt<strong>AI</strong></span>
                    </div>
                    <div className="nav-actions">
                        <span className="nav-tag">Sales Insight Automator</span>
                        <button 
                            className="theme-toggle" 
                            onClick={toggleTheme}
                            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
                            title="Toggle theme"
                        >
                            {theme === 'dark' ? (
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
                            ) : (
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                            )}
                        </button>
                    </div>
                </div>
            </header>

            {/* ── Hero ────────────────────────────────────────────────── */}
            <section className="hero">
                <div className="hero-badge">✦ Powered by Groq · Llama 3.3 70B</div>
                <h1 className="hero-title">
                    Turn Raw Sales Data<br />
                    Into <span className="hero-accent">Executive Insights</span>
                </h1>
                <p className="hero-sub">
                    Upload a CSV or XLSX file. Our AI distils it into a crisp,
                    professional narrative — delivered straight to your inbox in seconds.
                </p>
            </section>

            {/* ── Upload Card ─────────────────────────────────────────── */}
            <main className="main-content">
                <UploadForm />
            </main>

            {/* ── Footer ──────────────────────────────────────────────── */}
            <footer className="footer">
                <p>© {new Date().getFullYear()} Rabbitt AI · Built with FastAPI + Gemini</p>
            </footer>
        </div>
    )
}
