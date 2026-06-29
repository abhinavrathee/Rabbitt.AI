import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { uploadFile } from '../api/client.js'
import StatusBanner from './StatusBanner.jsx'
import './UploadForm.css'

const ACCEPTED_TYPES = {
    'text/csv': ['.csv'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/octet-stream': ['.csv', '.xlsx'],
}

export default function UploadForm() {
    const [file, setFile] = useState(null)
    const [email, setEmail] = useState('')
    const [status, setStatus] = useState('idle') // idle | loading | success | error
    const [message, setMessage] = useState('')
    const [preview, setPreview] = useState('')
    const [progress, setProgress] = useState(0)

    /* ── Dropzone ─────────────────────────────────────────── */
    const onDrop = useCallback((accepted, rejected) => {
        if (rejected.length > 0) {
            setStatus('error')
            setMessage('Only .csv and .xlsx files up to 5 MB are accepted.')
            setFile(null)
            return
        }
        setFile(accepted[0])
        setStatus('idle')
        setMessage('')
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: ACCEPTED_TYPES,
        maxFiles: 1,
        maxSize: 5 * 1024 * 1024,
    })

    /* ── Submit ───────────────────────────────────────────── */
    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!file) { setStatus('error'); setMessage('Please select a file.'); return }
        if (!email.trim()) { setStatus('error'); setMessage('Please enter an email address.'); return }

        setStatus('loading')
        setProgress(0)
        setMessage('')
        setPreview('')

        try {
            const data = await uploadFile(file, email, setProgress)
            setStatus('success')
            setMessage(data.message)
            setPreview(data.summary_preview)
        } catch (err) {
            setStatus('error')
            const detail = err?.response?.data?.detail
            setMessage(typeof detail === 'string' ? detail : 'Something went wrong. Please try again.')
        }
    }

    /* ── Reset ────────────────────────────────────────────── */
    const reset = () => {
        setFile(null); setEmail(''); setStatus('idle')
        setMessage(''); setPreview(''); setProgress(0)
    }

    /* ── Render ───────────────────────────────────────────── */
    return (
        <div className="card">
            <StatusBanner status={status} message={message} preview={preview} onReset={reset} />

            {status !== 'success' && (
                <form onSubmit={handleSubmit} noValidate id="upload-form">
                    {/* Dropzone */}
                    <div
                        {...getRootProps()}
                        className={`dropzone ${isDragActive ? 'dropzone--active' : ''} ${file ? 'dropzone--filled' : ''}`}
                        role="button"
                        aria-label="File upload area"
                        id="file-dropzone"
                    >
                        <input {...getInputProps()} id="file-input" />
                        <div className="dropzone-icon" aria-hidden="true">
                            {file ? '📄' : isDragActive ? '📂' : '⬆️'}
                        </div>
                        {file ? (
                            <div className="dropzone-file-info">
                                <span className="file-name">{file.name}</span>
                                <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
                            </div>
                        ) : (
                            <>
                                <p className="dropzone-label">
                                    {isDragActive ? 'Drop it here!' : 'Drag & drop your file here'}
                                </p>
                                <p className="dropzone-hint">or click to browse · .csv · .xlsx · max 5 MB</p>
                            </>
                        )}
                    </div>

                    {/* Email field */}
                    <div className="field-group">
                        <label htmlFor="email-input" className="field-label">
                            Recipient email
                        </label>
                        <input
                            id="email-input"
                            type="email"
                            className="field-input"
                            placeholder="exec@company.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            autoComplete="email"
                        />
                    </div>

                    {/* Progress bar (visible during upload) */}
                    {status === 'loading' && (
                        <div className="progress-wrap" role="progressbar" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
                            <div className="progress-bar" style={{ width: `${Math.max(progress, 5)}%` }} />
                            <span className="progress-label">{progress < 100 ? `Uploading… ${progress}%` : 'Generating AI summary…'}</span>
                        </div>
                    )}

                    {/* Submit */}
                    <button
                        id="submit-btn"
                        type="submit"
                        className="btn-primary"
                        disabled={status === 'loading'}
                    >
                        {status === 'loading' ? (
                            <><span className="spinner" aria-hidden="true" /> Processing…</>
                        ) : (
                            '✦ Generate & Send Summary'
                        )}
                    </button>
                </form>
            )}

            {/* Step guide */}
            {status === 'idle' && (
                <ol className="steps">
                    <li><span>1</span> Upload your sales CSV or Excel file</li>
                    <li><span>2</span> Enter the recipient's email</li>
                    <li><span>3</span> Gemini AI analyses the data &amp; sends the brief</li>
                </ol>
            )}
        </div>
    )
}
