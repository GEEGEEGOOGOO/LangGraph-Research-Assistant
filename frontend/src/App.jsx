import { useState } from 'react'
import Navbar from './components/Navbar'
import HeroSection from './components/HeroSection'
import QueryPanel from './components/QueryPanel'
import GraphView from './components/GraphView'
import UploadModal from './components/UploadModal'
import SettingsDrawer from './components/SettingsDrawer'
import Footer from './components/Footer'

function App() {
    const [showUploadModal, setShowUploadModal] = useState(false)
    const [showSettings, setShowSettings] = useState(false)
    const [darkMode, setDarkMode] = useState(true)
    const [graphData, setGraphData] = useState(null)
    const [queryResponse, setQueryResponse] = useState(null)

    return (
        <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
            <div className="dark:bg-navy bg-gray-50 dark:text-white text-gray-900 min-h-screen">
                <Navbar
                    onUpload={() => setShowUploadModal(true)}
                    onSettings={() => setShowSettings(true)}
                />

                <HeroSection
                    onGetStarted={() => document.getElementById('query-section').scrollIntoView({ behavior: 'smooth' })}
                    onUpload={() => setShowUploadModal(true)}
                />

                <div id="query-section" className="container mx-auto px-4 py-12">
                    <div className="grid lg:grid-cols-2 gap-6">
                        <QueryPanel
                            onResponse={setQueryResponse}
                            onGraphUpdate={setGraphData}
                        />
                        <GraphView graphData={graphData} />
                    </div>
                </div>

                <Footer />

                {showUploadModal && (
                    <UploadModal
                        onClose={() => setShowUploadModal(false)}
                        onUploadComplete={(data) => {
                            setGraphData(data)
                            setShowUploadModal(false)
                        }}
                    />
                )}

                {showSettings && (
                    <SettingsDrawer
                        onClose={() => setShowSettings(false)}
                        darkMode={darkMode}
                        onToggleDarkMode={() => setDarkMode(!darkMode)}
                    />
                )}
            </div>
        </div>
    )
}

export default App
