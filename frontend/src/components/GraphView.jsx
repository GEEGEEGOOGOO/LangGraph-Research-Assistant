import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { ZoomIn, ZoomOut, Maximize2, Download } from 'lucide-react'

export default function GraphView({ graphData }) {
    const svgRef = useRef(null)
    const [showLabels, setShowLabels] = useState(true)

    useEffect(() => {
        if (!graphData || !svgRef.current) return

        const svg = d3.select(svgRef.current)
        svg.selectAll('*').remove()

        const width = svgRef.current.clientWidth
        const height = svgRef.current.clientHeight

        // Create sample graph data if none provided
        const nodes = graphData.nodes || [
            { id: 'MCP', group: 1 },
            { id: 'RAG', group: 1 },
            { id: 'LangGraph', group: 2 },
            { id: 'Gemini', group: 2 },
            { id: 'Knowledge Graph', group: 3 },
        ]

        const links = graphData.links || [
            { source: 'MCP', target: 'RAG' },
            { source: 'RAG', target: 'LangGraph' },
            { source: 'LangGraph', target: 'Gemini' },
            { source: 'Gemini', target: 'Knowledge Graph' },
            { source: 'Knowledge Graph', target: 'RAG' },
        ]

        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))

        const g = svg.append('g')

        // Add zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.5, 3])
            .on('zoom', (event) => {
                g.attr('transform', event.transform)
            })

        svg.call(zoom)

        // Draw links
        const link = g.append('g')
            .selectAll('line')
            .data(links)
            .join('line')
            .attr('stroke', '#6366f1')
            .attr('stroke-opacity', 0.6)
            .attr('stroke-width', 2)

        // Draw nodes
        const node = g.append('g')
            .selectAll('circle')
            .data(nodes)
            .join('circle')
            .attr('r', 12)
            .attr('fill', d => d3.schemeCategory10[d.group])
            .attr('stroke', '#fff')
            .attr('stroke-width', 2)
            .style('cursor', 'pointer')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended))

        // Add labels
        const label = g.append('g')
            .selectAll('text')
            .data(nodes)
            .join('text')
            .text(d => d.id)
            .attr('font-size', 12)
            .attr('dx', 15)
            .attr('dy', 4)
            .attr('fill', '#fff')
            .style('pointer-events', 'none')
            .style('display', showLabels ? 'block' : 'none')

        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y)

            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y)

            label
                .attr('x', d => d.x)
                .attr('y', d => d.y)
        })

        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart()
            event.subject.fx = event.subject.x
            event.subject.fy = event.subject.y
        }

        function dragged(event) {
            event.subject.fx = event.x
            event.subject.fy = event.y
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0)
            event.subject.fx = null
            event.subject.fy = null
        }

    }, [graphData, showLabels])

    return (
        <div className="glass-dark rounded-xl p-6 h-[600px] relative">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-heading font-bold">Knowledge Graph</h2>

                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setShowLabels(!showLabels)}
                        className="px-3 py-2 bg-navy/50 hover:bg-navy/70 rounded-lg text-sm transition-colors"
                    >
                        {showLabels ? 'Hide' : 'Show'} Labels
                    </button>

                    <button className="p-2 bg-navy/50 hover:bg-navy/70 rounded-lg transition-colors">
                        <ZoomIn className="w-5 h-5" />
                    </button>

                    <button className="p-2 bg-navy/50 hover:bg-navy/70 rounded-lg transition-colors">
                        <ZoomOut className="w-5 h-5" />
                    </button>

                    <button className="p-2 bg-navy/50 hover:bg-navy/70 rounded-lg transition-colors">
                        <Maximize2 className="w-5 h-5" />
                    </button>

                    <button className="p-2 bg-navy/50 hover:bg-navy/70 rounded-lg transition-colors">
                        <Download className="w-5 h-5" />
                    </button>
                </div>
            </div>

            <svg
                ref={svgRef}
                className="w-full h-[calc(100%-60px)] bg-navy/30 rounded-lg"
            />
        </div>
    )
}
