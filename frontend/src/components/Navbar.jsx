import { Network, Settings, FileUp, BookOpen } from 'lucide-react'

export default function Navbar({ onUpload, onSettings }) {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass-dark border-b border-white/10">
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <div className="flex items-center space-x-3">
                        <Network className="w-8 h-8 text-primary" />
                        <span className="text-xl font-heading font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                            LangGraph Research Assistant
                        </span>
                    </div>

                    {/* Nav Links */}
                    <div className="hidden md:flex items-center space-x-6">
                        <button className="flex items-center space-x-2 hover:text-primary transition-colors">
                            <BookOpen className="w-5 h-5" />
                            <span>Docs</span>
                        </button>

                        <button
                            onClick={onUpload}
                            className="flex items-center space-x-2 hover:text-primary transition-colors"
                        >
                            <FileUp className="w-5 h-5" />
                            <span>Add Document</span>
                        </button>

                        <button
                            onClick={() => document.getElementById('query-section')?.scrollIntoView({ behavior: 'smooth' })}
                            className="flex items-center space-x-2 hover:text-primary transition-colors"
                        >
                            <Network className="w-5 h-5" />
                            <span>Graph View</span>
                        </button>

                        <button
                            onClick={onSettings}
                            className="flex items-center space-x-2 hover:text-primary transition-colors"
                        >
                            <Settings className="w-5 h-5" />
                            <span>Settings</span>
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    )
}
