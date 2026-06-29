import './StatusBanner.css'

export default function StatusBanner({ status, message, preview, onReset }) {
    if (status === 'idle') return null

    return (
        <div className={`banner banner--${status}`} role="alert" aria-live="polite">
            {status === 'loading' && (
                <div className="banner-loading">
                    <span className="banner-icon">⚙️</span>
                    <p>Analysing your data with Gemini AI…</p>
                </div>
            )}

            {status === 'success' && (
                <div className="banner-success">
                    <div className="banner-check">✓</div>
                    <h2>Summary Sent!</h2>
                    <p>{message}</p>
                    {preview && (
                        <div className="preview-box">
                            <p className="preview-label">Preview snippet:</p>
                            <p className="preview-text">{preview}</p>
                        </div>
                    )}
                    <button className="btn-outline" onClick={onReset} id="try-again-btn">
                        ← Upload another file
                    </button>
                </div>
            )}

            {status === 'error' && (
                <div className="banner-error">
                    <span className="banner-icon-err">⚠</span>
                    <p>{message}</p>
                </div>
            )}
        </div>
    )
}
