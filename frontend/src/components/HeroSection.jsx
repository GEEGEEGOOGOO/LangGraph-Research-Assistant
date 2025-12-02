import { ArrowRight, FileUp } from 'lucide-react'
import { useEffect, useRef } from 'react'

export default function HeroSection({ onGetStarted, onUpload }) {
    const canvasRef = useRef(null)

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return

        const ctx = canvas.getContext('2d')
        canvas.width = canvas.offsetWidth
        canvas.height = canvas.offsetHeight

        // Simple animated network background
        const nodes = Array.from({ length: 30 }, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
        }))

        function animate() {
            ctx.fillStyle = 'rgba(15, 23, 42, 0.1)'
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            // Update and draw nodes
            nodes.forEach(node => {
                node.x += node.vx
                node.y += node.vy

                if (node.x < 0 || node.x > canvas.width) node.vx *= -1
                if (node.y < 0 || node.y > canvas.height) node.vy *= -1

                ctx.beginPath()
                ctx.arc(node.x, node.y, 2, 0, Math.PI * 2)
                ctx.fillStyle = 'rgba(99, 102, 241, 0.6)'
                ctx.fill()
            })

            // Draw connections
            nodes.forEach((node, i) => {
                nodes.slice(i + 1).forEach(other => {
                    const dist = Math.hypot(node.x - other.x, node.y - other.y)
                    if (dist < 150) {
                        ctx.beginPath()
                        ctx.moveTo(node.x, node.y)
                        ctx.lineTo(other.x, other.y)
                        ctx.strokeStyle = `rgba(99, 102, 241, ${0.2 * (1 - dist / 150)})`
                        ctx.stroke()
                    }
                })
            })

            requestAnimationFrame(animate)
        }

        animate()
    }, [])

    return (
        <div className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
            <canvas
                ref={canvasRef}
                className="absolute inset-0 w-full h-full"
            />

            <div className="relative z-10 text-center px-4 max-w-4xl">
                <h1 className="text-6xl md:text-7xl font-heading font-bold mb-6 bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent animate-float">
                    Your Knowledge Graph-Powered Research Assistant
                </h1>

                <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto">
                    Explore connections between ideas — not just keywords.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <button
                        onClick={onGetStarted}
                        className="px-8 py-4 bg-primary hover:bg-primary/80 rounded-lg font-semibold flex items-center justify-center space-x-2 neon-glow-hover transition-all"
                    >
                        <span>Start Exploring</span>
                        <ArrowRight className="w-5 h-5" />
                    </button>

                    <button
                        onClick={onUpload}
                        className="px-8 py-4 glass-dark hover:bg-white/20 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-all"
                    >
                        <FileUp className="w-5 h-5" />
                        <span>Add Your First Document</span>
                    </button>
                </div>
            </div>
        </div>
    )
}
