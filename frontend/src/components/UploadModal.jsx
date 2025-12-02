import { useState } from 'react'
import { X, Upload, FileText, Loader } from 'lucide-react'

export default function UploadModal({ onClose, onUploadComplete }) {
    const [file, setFile] = useState(null)
    const [text, setText] = useState('')
    const [title, setTitle] = useState('')
    const [uploading, setUploading] = useState(false)
    const [progress, setProgress] = useState('')

    const handleUpload = async () => {
        if (!file && !text.trim()) return

        setUploading(true)
        setProgress('Extracting entities...')

        try {
            const formData = new FormData()
            if (file) {
                formData.append('file', file)
            } else {
                formData.append('text', text)
            }
            formData.append('title', title)

            setTimeout(() => setProgress('Building relationships...'), 1000)

            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            })

            const data = await res.json()
            setProgress('Complete!')

            setTimeout(() => {
                onUploadComplete?.(data)
            }, 500)

        } catch (error) {
            console.error('Upload failed:', error)
            setProgress('Error: Upload failed')
        } finally {
            setTimeout(() => setUploading(false), 1500)
        }
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
            <div className="glass-dark rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-heading font-bold">Add Document</h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <div className="space-y-6">
                    {/* Title */}
                    <div>
                        <label className="block text-sm font-semibold mb-2">Title (Optional)</label>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            placeholder="Document title..."
                            className="w-full px-4 py-3 bg-navy/50 border border-white/10 rounded-lg focus:outline-none focus:border-primary"
                        />
                    </div>

                    {/* File Upload */}
                    <div>
                        <label className="block text-sm font-semibold mb-2">Upload File</label>
                        <div className="border-2 border-dashed border-white/20 rounded-lg p-8 text-center hover:border-primary/50 transition-colors">
                            <input
                                type="file"
                                onChange={(e) => setFile(e.target.files[0])}
                                accept=".pdf,.txt,.md"
                                className="hidden"
                                id="file-upload"
                            />
                            <label htmlFor="file-upload" className="cursor-pointer">
                                <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                                <p className="text-gray-300">
                                    {file ? file.name : 'Click to upload PDF, TXT, or MD file'}
                                </p>
                            </label>
                        </div>
                    </div>

                    <div className="text-center text-gray-400">— OR —</div>

                    {/* Text Input */}
                    <div>
                        <label className="block text-sm font-semibold mb-2">Paste Content</label>
                        <textarea
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Paste your text here..."
                            rows={8}
                            className="w-full px-4 py-3 bg-navy/50 border border-white/10 rounded-lg focus:outline-none focus:border-primary resize-none"
                        />
                    </div>

                    {/* Progress */}
                    {uploading && (
                        <div className="p-4 bg-primary/20 border border-primary/30 rounded-lg flex items-center space-x-3">
                            <Loader className="w-5 h-5 animate-spin" />
                            <span>{progress}</span>
                        </div>
                    )}

                    {/* Actions */}
                    <div className="flex space-x-4">
                        <button
                            onClick={onClose}
                            className="flex-1 px-6 py-3 bg-gray-600 hover:bg-gray-700 rounded-lg font-semibold transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleUpload}
                            disabled={uploading || (!file && !text.trim())}
                            className="flex-1 px-6 py-3 bg-primary hover:bg-primary/80 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-semibold flex items-center justify-center space-x-2 transition-all neon-glow-hover"
                        >
                            <FileText className="w-5 h-5" />
                            <span>Build Knowledge Graph</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
