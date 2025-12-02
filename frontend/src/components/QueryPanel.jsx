import { useState } from 'react'
import { Search, ChevronDown, ChevronUp } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function QueryPanel({ onResponse, onGraphUpdate }) {
    const [query, setQuery] = useState('')
    const [hops, setHops] = useState(2)
    const [loading, setLoading] = useState(false)
    const [response, setResponse] = useState(null)
    const [showContext, setShowContext] = useState(false)

    const handleQuery = async () => {
        if (!query.trim()) return

        setLoading(true)
        try {
            const res = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, hops })
            })

            const data = await res.json()
            setResponse(data)
            onResponse?.(data)
            onGraphUpdate?.(data.graph_data)
        } catch (error) {
            console.error('Query failed:', error)
            setResponse({
                final_answer: 'Error: Could not connect to backend. Make sure the API server is running on port 8000.',
                retrieved_docs: []
            })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="glass-dark rounded-xl p-6 h-fit">
            <h2 className="text-2xl font-heading font-bold mb-6">Query Your Knowledge Graph</h2>

            {/* Query Input */}
            <div className="space-y-4">
                <div className="relative">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
                        placeholder="Ask me anything about your knowledge base..."
                        className="w-full px-4 py-3 bg-navy/50 border border-white/10 rounded-lg focus:outline-none focus:border-primary transition-colors"
                    />
                </div>

                <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                        <label className="text-sm text-gray-400">Traversal Hops:</label>
                        <select
                            value={hops}
                            onChange={(e) => setHops(Number(e.target.value))}
                            className="px-3 py-2 bg-navy/50 border border-white/10 rounded-lg focus:outline-none focus:border-primary"
                        >
                            <option value={1}>1</option>
                            <option value={2}>2</option>
                            <option value={3}>3</option>
                        </select>
                    </div>

                    <button
                        onClick={handleQuery}
                        disabled={loading || !query.trim()}
                        className="flex-1 px-6 py-3 bg-primary hover:bg-primary/80 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-semibold flex items-center justify-center space-x-2 transition-all neon-glow-hover"
                    >
                        <Search className="w-5 h-5" />
                        <span>{loading ? 'Searching...' : 'Search'}</span>
                    </button>
                </div>
            </div>

            {/* Response Area */}
            {response && (
                <div className="mt-6 space-y-4">
                    <div className="p-4 bg-navy/50 rounded-lg border border-primary/30">
                        <h3 className="text-lg font-semibold mb-3 text-primary">Answer</h3>
                        <div className="prose prose-invert max-w-none">
                            <ReactMarkdown>{response.final_answer || 'No answer generated.'}</ReactMarkdown>
                        </div>
                    </div>

                    {/* Retrieved Context */}
                    {response.retrieved_docs && response.retrieved_docs.length > 0 && (
                        <div className="border border-white/10 rounded-lg overflow-hidden">
                            <button
                                onClick={() => setShowContext(!showContext)}
                                className="w-full px-4 py-3 bg-navy/30 hover:bg-navy/50 flex items-center justify-between transition-colors"
                            >
                                <span className="font-semibold">Retrieved Graph Context ({response.retrieved_docs.length})</span>
                                {showContext ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                            </button>

                            {showContext && (
                                <div className="p-4 space-y-2">
                                    {response.retrieved_docs.map((doc, idx) => (
                                        <div key={idx} className="p-3 bg-navy/50 rounded border border-white/5">
                                            <span className="text-sm text-gray-300">{doc}</span>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
