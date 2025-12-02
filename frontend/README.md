# LangGraph Research Assistant - Frontend

A beautiful, futuristic UI for the LangGraph Research Assistant powered by GraphRAG and Gemini 2.5 Flash.

## Features

- 🎨 **Stunning UI** with animated network background
- 📊 **Interactive Graph Visualization** using D3.js
- 🔍 **Smart Query Interface** with configurable traversal depth
- 📤 **Document Upload** with drag-and-drop support
- ⚙️ **Settings Panel** for customization
- 🌙 **Dark Mode** (default)
- 📱 **Fully Responsive** design

## Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The frontend will start on `http://localhost:3000` and proxy API requests to `http://localhost:8000`.

### Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── HeroSection.jsx
│   │   ├── QueryPanel.jsx
│   │   ├── GraphView.jsx
│   │   ├── UploadModal.jsx
│   │   ├── SettingsDrawer.jsx
│   │   └── Footer.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## API Endpoints

The frontend expects the following backend endpoints:

- `POST /api/query` - Query the knowledge graph
- `POST /api/upload` - Upload documents
- `GET /api/graph` - Get graph data

## Technologies

- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **D3.js** - Graph visualization
- **React Markdown** - Markdown rendering
- **Lucide React** - Icons

## Customization

Edit `tailwind.config.js` to customize colors and theme:

```js
colors: {
  primary: '#6366f1',  // Electric blue
  accent: '#8b5cf6',   // Violet
  navy: '#0f172a',     // Deep navy
}
```

## License

MIT
