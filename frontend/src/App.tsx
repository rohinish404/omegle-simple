import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Landing } from './components/Landing'
function App() {
  
  return (
    <Router>
    <div className="min-h-screen bg-gray-100">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Landing />} />
        </Routes>
      </main>
    </div>
  </Router>
  )
}

export default App
