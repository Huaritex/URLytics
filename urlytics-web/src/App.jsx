import { useState, useEffect } from 'react'
import GridDistortion from './components/GridDistortion'
import './App.css'

const GRID_TEXTURE_LIGHT = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc0MDAnIGhlaWdodD0nNDAwJz4KPGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0nZ3JhZCcgeDE9JzAlJyB5MT0nMCUnIHgyPScxMDAlJyB5Mj0nMTAwJSc+CjxzdG9wIG9mZnNldD0nMCUnIHN0eWxlPSdzdG9wLWNvbG9yOiMwMDAwMDA7c3RvcC1vcGFjaXR5OjEnIC8+CjxzdG9wIG9mZnNldD0nMTAwJScgc3R5bGU9J3N0b3AtY29sb3I6IzAwN2JmZjtzdG9wLW9wYWNpdHk6MScgLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8cmVjdCB3aWR0aD0nNDAwJyBoZWlnaHQ9JzQwMCcgZmlsbD0ndXJsKCNncmFkKScvPgo8cGF0aCBkPSdNMCAwIEwwIDQwMC BNNTAgMC BMNTAgNDAwIE0xMDAgMC BMMTAwIDQwMC BNMTUwIDAgTDE1MCA0MDAgTTIwMCAwIEwyMDA gNDAw IE0yNTAgMC BMMjUw IDQwMC BNMzAw IDAgTDMwMCA0MDAtTTM1MCAw IEwzNTAgNDAw IE00MDA gMC BMNDAw IDQwMCcgc3Ryb2tlPSdyZ2JhKDAsMTIzLDI1NSwwLjM1KScgc3Ryb2tlLXdpZHRoPScxJy8+CjxwYXRoIGQ9J00wIDAgTDQwMCAwIE0wIDUw IEw0MDAgNTAgTTAgMTAw IEw0MDAgMTAw IE0wIDE1MC BMNDAwIDE1MC BNMCAyMDA gTDQwMCAyMDA gTTAgMjUw IEw0MDAgMjUw IE0wIDMwMC BMNDAw IDMwMC BNMCAzNTAgTDQwMCAzNTAgTTAgNDAwIEw0MDAgNDAwJyBzdHJva2U9J3JnYmEoMCwxMjMsMjU1LDAuMzUpJyBzdHJva2Utd2lkdGg9JzEnLz4KPC9zdmc+"
const GRID_TEXTURE_DARK = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc0MDAnIGhlaWdodD0nNDAwJz4KPGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0nZ3JhZCcgeDE9JzAlJyB5MT0nMCUnIHgyPScxMDAlJyB5Mj0nMTAwJSc+CjxzdG9wIG9mZnNldD0nMCUnIHN0eWxlPSdzdG9wLWNvbG9yOiNmZmZmZmY7c3RvcC1vcGFjaXR5OjEnIC8+CjxzdG9wIG9mZnNldD0nMTAwJScgc3R5bGU9J3N0b3AtY29sb3I6I2ZmMDBmZjtzdG9wLW9wYWNpdHk6MScgLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8cmVjdCB3aWR0aD0nNDAwJyBoZWlnaHQ9JzQwMCcgZmlsbD0ndXJsKCNncmFkKScvPgo8cGF0aCBkPSdNMCAwIEwwIDQwMC BNNTAgMC BMNTAgNDAw IE0xMDA gMC BMMTAw IDQwMC BNMTUw IDAgTDE1MCA0MDAgTTIwMCAw IEwyMDA gNDAw IE0yNTAgMC BMMjUw IDQwMC BNMzAw IDAgTDMwMCA0MDAtTTM1MCAw IEwzNTAgNDAw IE00MDA gMC BMNDAw IDQwMCcgc3Ryb2tlPSdyZ2JhKDI1NSwwLDI1NSwwLjM1KScgc3Ryb2tlLXdpZHRoPScxJy8+CjxwYXRoIGQ9J00w IDAgTDQwMCAw IE0wIDUw IEw0MDAgNTAgTTAgMTAw IEw0MDAgMTAw IE0wIDE1MC BMNDAwIDE1MC BNMCAyMDA gTDQwMCAyMDA gTTAgMjUw IEw0MDAgMjUw IE0wIDMwMC BMNDAw IDMwMC BNMCAzNTAgTDQwMCAzNTAgTTAgNDAwIEw0MDAgNDAwJyBzdHJva2U9J3JnYmEoMjU1LDAsMjU1LDAuMzUpJyBzdHJva2Utd2lkdGg9JzEnLz4KPC9zdmc+"

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isActive, setIsActive] = useState(true)
  const [textToAnalyze, setTextToAnalyze] = useState('')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [alert, setAlert] = useState(null)

  useEffect(() => {
    // Check for dark mode preference
    const isDark = localStorage.getItem('theme') === 'dark' || 
      (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
    setIsDarkMode(isDark)
    if (isDark) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
    document.documentElement.classList.toggle('dark')
    localStorage.setItem('theme', !isDarkMode ? 'dark' : 'light')
  }

  const showAlert = (message, type = 'info', duration = 3000) => {
    setAlert({ message, type })
    setTimeout(() => setAlert(null), duration)
  }

  const analyzeText = async () => {
    if (!isActive) {
      showAlert('URLytics está desactivado. Actívalo para analizar mensajes.', 'info')
      setAnalysisResult(null)
      return
    }

    if (!textToAnalyze.trim()) {
      showAlert('Por favor, ingresa texto para analizar.', 'warning')
      setAnalysisResult(null)
      return
    }

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textToAnalyze })
      })

      if (!response.ok) throw new Error('Error en la API')

      const result = await response.json()
      const isPhishing = result.prediction === 1 && result.confidence >= 0.25

      setAnalysisResult({
        isSuspicious: isPhishing,
        type: isPhishing ? 'Phishing' : 'No Phishing',
        message: isPhishing ? '¡Alerta! Posible phishing.' : 'Parece seguro.',
        details: `Confianza: ${(result.confidence * 100).toFixed(2)}%`,
        score: result.confidence
      })
    } catch (error) {
      showAlert('No se pudo conectar con el backend de IA.', 'error')
    }
  }

  const getAlertStyles = (type) => {
    const styles = {
      error: 'bg-red-100 dark:bg-red-900/50 border-red-400 dark:border-red-600 text-red-700 dark:text-red-300',
      warning: 'bg-yellow-100 dark:bg-yellow-900/50 border-yellow-400 dark:border-yellow-500 text-yellow-700 dark:text-yellow-300',
      info: 'bg-blue-100 dark:bg-blue-900/50 border-blue-400 dark:border-blue-500 text-blue-700 dark:text-blue-300',
      success: 'bg-green-100 dark:bg-green-900/50 border-green-400 dark:border-green-500 text-green-700 dark:text-green-300'
    }
    return styles[type] || styles.info
  }

  const gridTexture = isDarkMode ? GRID_TEXTURE_LIGHT : GRID_TEXTURE_DARK
  const baseGradientClass = isDarkMode
    ? 'from-white via-fuchsia-50 to-pink-200'
    : 'from-black via-slate-900 to-blue-600'
  const overlayGradientClass = isDarkMode
    ? 'from-fuchsia-400/50 via-transparent to-rose-300/40'
    : 'from-blue-500/40 via-transparent to-cyan-300/20'

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      <div className={`absolute inset-0 -z-30 bg-gradient-to-br ${baseGradientClass}`} />
      <GridDistortion
        className="absolute inset-0 -z-20"
        imageSrc={gridTexture}
        grid={25}
        mouse={0.35}
        strength={0.2}
        relaxation={0.92}
        trackingTarget="window"
      />
      <div className={`absolute inset-0 -z-10 bg-gradient-to-r mix-blend-screen ${overlayGradientClass}`} />

      <div className="relative z-10 flex min-h-screen items-center justify-center p-4">
        <div className="w-full max-w-md bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg rounded-xl shadow-2xl p-6 md:p-8 transition-colors duration-300">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <svg className="w-10 h-10 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
            </svg>
            <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100">URLytics</h1>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleDarkMode}
              className="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5"
            >
              {isDarkMode ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm-.707 8.486a1 1 0 011.414 0l.707.707a1 1 0 01-1.414 1.414l-.707-.707a1 1 0 010-1.414zM4 11a1 1 0 100-2H3a1 1 0 100 2h1z" fillRule="evenodd" clipRule="evenodd"></path>
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                </svg>
              )}
            </button>
            <label className="relative inline-block w-12 h-6">
              <input
                type="checkbox"
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
                className="opacity-0 w-0 h-0 peer"
              />
              <span className="absolute cursor-pointer inset-0 bg-gray-300 dark:bg-gray-600 rounded-full transition-all peer-checked:bg-blue-600 before:absolute before:content-[''] before:h-5 before:w-5 before:left-0.5 before:bottom-0.5 before:bg-white before:rounded-full before:transition-all peer-checked:before:translate-x-6"></span>
            </label>
          </div>
        </div>

        {/* Status Message */}
        <div className={`mb-6 p-3 rounded-lg text-center text-sm font-medium ${
          isActive 
            ? 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300'
            : 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300'
        }`}>
          {isActive ? 'URLytics está activo y protegiéndote.' : 'URLytics está desactivado.'}
        </div>

        {/* Alert Container */}
        {alert && (
          <div className={`mb-6 border-l-4 p-4 rounded-md shadow-md ${getAlertStyles(alert.type)} animate-fade-in`}>
            <p className="text-sm">{alert.message}</p>
          </div>
        )}

        {/* Text Analyzer */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Analizador de Mensajes</h2>
          <div>
            <label htmlFor="textToAnalyze" className="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
              Ingresa texto para analizar:
            </label>
            <textarea
              id="textToAnalyze"
              rows="4"
              value={textToAnalyze}
              onChange={(e) => setTextToAnalyze(e.target.value)}
              className="w-full p-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow"
              placeholder="Ej: 'Hola, haz clic en este enlace urgente...'"
            />
          </div>
          <button
            onClick={analyzeText}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Analizar Texto
          </button>
        </div>

        {/* Analysis Results */}
        {analysisResult && (
          <div className="mt-6 p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900/50 animate-fade-in">
            <h3 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-2">Resultado del Análisis:</h3>
            <p className={`text-sm mb-1 font-semibold ${
              analysisResult.isSuspicious 
                ? 'text-red-600 dark:text-red-400' 
                : 'text-green-600 dark:text-green-400'
            }`}>
              Nivel de Riesgo: {analysisResult.isSuspicious ? 'Alto' : 'Bajo'} (Score: {analysisResult.score.toFixed(2)})
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Detalles: {analysisResult.details}</p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 pt-4 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-500 text-center">
          <p>URLytics v2.3</p>
          <p>Este es un prototipo por lo cual puede tener errores</p>
          <p>By Huaritex</p>
        </div>
        </div>
      </div>
    </div>
  )
}

export default App
