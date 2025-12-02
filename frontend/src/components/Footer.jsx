import { Github } from 'lucide-react'

export default function Footer() {
    return (
        <footer className="border-t border-white/10 py-8 mt-20">
            <div className="container mx-auto px-4">
                <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
                    <p className="text-gray-400 text-sm">
                        © 2025 LangGraph Research Assistant • Built with Gemini 2.5 Flash & LangGraph
                    </p>

                    <a
                        href="https://github.com"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-2 text-gray-400 hover:text-primary transition-colors"
                    >
                        <Github className="w-5 h-5" />
                        <span>View on GitHub</span>
                    </a>
                </div>
            </div>
        </footer>
    )
}
