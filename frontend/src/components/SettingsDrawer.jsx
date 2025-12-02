import { X, Moon, Sun, Layers } from 'lucide-react'

export default function SettingsDrawer({ onClose, darkMode, onToggleDarkMode }) {
    return (
        <div className="fixed inset-0 z-50 flex justify-end">
            <div
                className="absolute inset-0 bg-black/50 backdrop-blur-sm"
                onClick={onClose}
            />

            <div className="relative glass-dark w-full max-w-md h-full p-8 overflow-y-auto">
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-2xl font-heading font-bold">Settings</h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <div className="space-y-6">
                    {/* Dark Mode Toggle */}
                    <div className="flex items-center justify-between p-4 bg-navy/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            {darkMode ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
                            <span className="font-semibold">Dark Mode</span>
                        </div>
                        <button
                            onClick={onToggleDarkMode}
                            className={`relative w-14 h-7 rounded-full transition-colors ${darkMode ? 'bg-primary' : 'bg-gray-600'
                                }`}
                        >
                            <div
                                className={`absolute top-1 left-1 w-5 h-5 bg-white rounded-full transition-transform ${darkMode ? 'translate-x-7' : ''
                                    }`}
                            />
                        </button>
                    </div>

                    {/* Gemini Model */}
                    <div className="p-4 bg-navy/30 rounded-lg">
                        <label className="block text-sm font-semibold mb-3">Gemini Model</label>
                        <select className="w-full px-4 py-2 bg-navy/50 border border-white/10 rounded-lg focus:outline-none focus:border-primary">
                            <option>gemini-2.5-flash</option>
                            <option>gemini-1.5-pro</option>
                            <option>gemini-1.5-flash</option>
                        </select>
                    </div>

                    {/* Default Traversal Depth */}
                    <div className="p-4 bg-navy/30 rounded-lg">
                        <label className="block text-sm font-semibold mb-3">Default Traversal Depth</label>
                        <div className="flex items-center space-x-4">
                            <input
                                type="range"
                                min="1"
                                max="5"
                                defaultValue="2"
                                className="flex-1"
                            />
                            <span className="text-sm font-mono">2 hops</span>
                        </div>
                    </div>

                    {/* Auto-expand Graph */}
                    <div className="flex items-center justify-between p-4 bg-navy/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <Layers className="w-5 h-5" />
                            <span className="font-semibold">Auto-expand Graph</span>
                        </div>
                        <button className="relative w-14 h-7 rounded-full bg-gray-600">
                            <div className="absolute top-1 left-1 w-5 h-5 bg-white rounded-full" />
                        </button>
                    </div>

                    {/* API Endpoint */}
                    <div className="p-4 bg-navy/30 rounded-lg">
                        <label className="block text-sm font-semibold mb-3">API Endpoint</label>
                        <input
                            type="text"
                            defaultValue="http://localhost:8000"
                            className="w-full px-4 py-2 bg-navy/50 border border-white/10 rounded-lg focus:outline-none focus:border-primary font-mono text-sm"
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}
