import axios from 'axios'

const api = axios.create({
    baseURL: '/api',
    timeout: 120_000, // AI generation can take a few seconds
})

/**
 * Upload a sales file and trigger AI summary + email delivery.
 *
 * @param {File}   file  - The CSV or XLSX file to upload
 * @param {string} email - Recipient email address
 * @param {function} onProgress - Optional progress callback (0-100)
 * @returns {Promise<{ message: string, summary_preview: string }>}
 */
export async function uploadFile(file, email, onProgress) {
    const form = new FormData()
    form.append('file', file)
    form.append('email', email)

    const { data } = await api.post('/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
            if (onProgress && e.total) {
                onProgress(Math.round((e.loaded / e.total) * 100))
            }
        },
    })

    return data
}
