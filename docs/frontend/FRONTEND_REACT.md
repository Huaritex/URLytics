# 🎨 URLytics - Frontend React con Background Interactivo

## 📋 Resumen

URLytics ha sido migrado de un prototipo HTML estático a una **aplicación React moderna** con un background interactivo 3D usando **GridDistortion** de react-bits.

---

## 🚀 Tecnologías Implementadas

### Stack Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 18.3.1 | Framework principal |
| **Vite** | 5.4.21 | Build tool y dev server |
| **Tailwind CSS** | 3.4.17 | Estilos y theming |
| **Three.js** | 0.171.0 | Renderizado 3D del background |
| **shadcn/ui** | Latest | Sistema de componentes |

### Componentes Clave

- **GridDistortion**: Background animado con distorsión de malla 3D
- **App.jsx**: Componente principal con lógica de UI y theming
- **Dark/Light Mode**: Sistema de temas con paletas personalizadas

---

## 🎨 Sistema de Theming

### Paleta de Colores

#### 🌙 Modo Oscuro
- **Base Gradient**: `from-white via-fuchsia-50 to-pink-200`
- **Overlay Gradient**: `from-fuchsia-400/50 via-transparent to-rose-300/40`
- **Grid Texture**: Blanco/Magenta con opacidad 35%
- **Color Scheme**: Rosa/Fucsia/Magenta

#### ☀️ Modo Claro
- **Base Gradient**: `from-black via-slate-900 to-blue-600`
- **Overlay Gradient**: `from-blue-500/40 via-transparent to-cyan-300/20`
- **Grid Texture**: Negro/Azul eléctrico con opacidad 35%
- **Color Scheme**: Negro/Azul/Cyan

### Texturas SVG

Las texturas del grid se generan mediante SVG base64 con gradientes lineales y líneas de cuadrícula:

```javascript
const GRID_TEXTURE_LIGHT = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0n..." // Negro/Azul
const GRID_TEXTURE_DARK = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0n..."  // Blanco/Magenta
```

---

## 🔧 Estructura del Proyecto

```
urlytics-web/
├── src/
│   ├── App.jsx                    # Componente principal
│   ├── main.jsx                   # Entry point
│   ├── App.css                    # Estilos globales
│   ├── index.css                  # Tailwind imports
│   ├── components/
│   │   ├── GridDistortion.jsx     # Background 3D interactivo
│   │   ├── GridDistortion.css     # Estilos del canvas
│   │   └── ui/                    # Componentes shadcn
│   └── lib/
│       └── utils.js               # Utilidades (cn helper)
├── public/                        # Assets estáticos
├── dist/                          # Build de producción
├── package.json                   # Dependencias
├── vite.config.js                 # Configuración Vite
├── tailwind.config.js             # Configuración Tailwind
├── postcss.config.js              # PostCSS config
├── jsconfig.json                  # JavaScript paths
└── components.json                # shadcn config
```

---

## 🎮 Background Interactivo

### GridDistortion Component

El background utiliza **Three.js** para crear una malla animada que reacciona al movimiento del mouse:

```jsx
<GridDistortion
  className="absolute inset-0 -z-20"
  imageSrc={gridTexture}          // Textura dinámica por tema
  grid={25}                        // 25x25 grid
  mouse={0.35}                     // Sensibilidad al mouse
  strength={0.2}                   // Fuerza de distorsión
  relaxation={0.92}                // Velocidad de retorno
  trackingTarget="window"          // Track mouse en toda la ventana
/>
```

### Capas del Background (z-index)

```jsx
// z-30: Capa base con gradiente
<div className="bg-gradient-to-br {baseGradientClass}" />

// z-20: GridDistortion con Three.js
<GridDistortion imageSrc={gridTexture} />

// z-10: Overlay con mix-blend-screen
<div className="bg-gradient-to-r mix-blend-screen {overlayGradientClass}" />

// z-10: Contenido (Card de URLytics)
<div className="relative z-10">...</div>
```

---

## 🛠️ Instalación y Desarrollo

### 1. Instalar Dependencias

```bash
cd "/home/huaritex/Desktop/social engineer/urlytics-web"
npm install
```

### 2. Modo Desarrollo

```bash
npm run dev
```

**Salida esperada:**
```
VITE v5.4.21  ready in 159 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 3. Build de Producción

```bash
npm run build
```

**Output:**
```
✓ 36 modules transformed.
dist/index.html                   0.58 kB │ gzip:   0.38 kB
dist/assets/index-*.css          21.01 kB │ gzip:   4.17 kB
dist/assets/index-*.js          641.74 kB │ gzip: 175.69 kB
✓ built in 2.26s
```

### 4. Preview del Build

```bash
npm run preview
```

---

## 🔌 Integración con API

### Configuración del Endpoint

La aplicación React se conecta a la API Flask en `http://localhost:5000`:

```javascript
const analyzeText = async () => {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: textToAnalyze })
    })
    
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
```

### Estados de la Aplicación

```javascript
const [isDarkMode, setIsDarkMode] = useState(false)      // Tema oscuro/claro
const [isActive, setIsActive] = useState(true)           // URLytics activo/inactivo
const [textToAnalyze, setTextToAnalyze] = useState('')   // Texto del usuario
const [analysisResult, setAnalysisResult] = useState(null) // Resultado del análisis
const [alert, setAlert] = useState(null)                 // Alertas/notificaciones
```

---

## 📱 Características de la UI

### 1. Header
- Logo SVG de escudo
- Título "URLytics"
- Toggle de Dark/Light mode
- Toggle de Activación/Desactivación

### 2. Indicador de Estado
- Verde: "URLytics está activo y protegiéndote"
- Amarillo: "URLytics está desactivado"

### 3. Analizador de Mensajes
- **Input**: Textarea para ingresar texto
- **Botón**: "Analizar Texto"
- **Validaciones**:
  - URLytics debe estar activo
  - Texto no puede estar vacío
  - Manejo de errores de red

### 4. Resultados del Análisis
- **Nivel de Riesgo**: Alto (rojo) / Bajo (verde)
- **Score**: Confianza del modelo (0.00 - 1.00)
- **Detalles**: Porcentaje de confianza formateado

### 5. Sistema de Alertas
- **Error**: Rojo - Fallos de conexión
- **Warning**: Amarillo - Validaciones
- **Info**: Azul - Información general
- **Success**: Verde - Operaciones exitosas

### 6. Footer
- Versión: URLytics v2.3
- Disclaimer de prototipo
- Créditos: By Huaritex

---

## 🎯 Funcionalidades Implementadas

### ✅ Theming Dinámico
- Persistencia de preferencia de tema en `localStorage`
- Detección automática del tema del sistema
- Transiciones suaves entre temas
- Paletas de colores personalizadas

### ✅ Background Interactivo
- Distorsión de malla 3D con mouse tracking
- Texturas SVG generadas dinámicamente
- Capas de gradientes con blend modes
- Rendimiento optimizado con Three.js

### ✅ Responsive Design
- Breakpoints de Tailwind (sm, md, lg, xl)
- Card centrado con max-width
- Padding adaptativo
- Backdrop blur para glassmorphism

### ✅ Estado y Validaciones
- Control de activación de URLytics
- Validación de entrada de usuario
- Manejo de errores de API
- Sistema de notificaciones

---

## 🐛 Troubleshooting

### El servidor de desarrollo no inicia

```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Errores de build

```bash
# Verificar versiones de Node
node --version  # Debe ser >= 18.0.0

# Limpiar cache de Vite
npm run build -- --force
```

### Background no se muestra

1. Verifica que Three.js esté instalado:
   ```bash
   npm list three
   ```

2. Revisa la consola del navegador para errores WebGL

3. Asegúrate de que `GridDistortion.jsx` esté importado correctamente

### API no responde

1. Verifica que el backend Flask esté corriendo:
   ```bash
   curl http://localhost:5000/health
   ```

2. Revisa CORS si hay problemas de red:
   ```javascript
   // En api.py, asegúrate de tener:
   from flask_cors import CORS
   CORS(app)
   ```

---

## 📊 Métricas de Rendimiento

### Bundle Size
- **HTML**: 0.58 kB (gzip: 0.38 kB)
- **CSS**: 21.01 kB (gzip: 4.17 kB)
- **JS**: 641.74 kB (gzip: 175.69 kB)

### Optimizaciones Posibles
1. **Code Splitting**: Dividir Three.js en chunk separado
2. **Lazy Loading**: Cargar GridDistortion solo cuando sea necesario
3. **Tree Shaking**: Revisar imports de Tailwind
4. **CDN**: Servir Three.js desde CDN

---

## 🔄 Próximos Pasos

### Mejoras Planeadas
- [ ] Añadir animaciones de entrada/salida
- [ ] Implementar PWA (Progressive Web App)
- [ ] Agregar tests unitarios con Vitest
- [ ] Optimizar bundle size con code splitting
- [ ] Añadir más temas personalizados
- [ ] Implementar internacionalización (i18n)

### Integraciones Futuras
- [ ] Chrome Extension para análisis en tiempo real
- [ ] Widget embebible para otros sitios
- [ ] API pública con rate limiting
- [ ] Dashboard de estadísticas

---

## 📚 Referencias

### Documentación Oficial
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Three.js Documentation](https://threejs.org/docs/)
- [shadcn/ui](https://ui.shadcn.com/)

### Componentes Utilizados
- [react-bits GridDistortion](https://github.com/react-bits)
- [Tailwind Dark Mode](https://tailwindcss.com/docs/dark-mode)

### Tutoriales Relacionados
- [Building Interactive 3D Backgrounds](https://threejs.org/manual/)
- [React + Vite Setup](https://vitejs.dev/guide/#scaffolding-your-first-vite-project)
- [Tailwind with React](https://tailwindcss.com/docs/guides/vite)

---

## 👥 Créditos

- **Desarrollo**: Huaritex
- **Framework**: React 18
- **Build Tool**: Vite 5
- **UI Library**: shadcn/ui
- **3D Graphics**: Three.js
- **Background Component**: react-bits GridDistortion

---

## 📄 Licencia

Este proyecto es parte de URLytics v2.3 - Sistema de detección de phishing con IA.

---

**Última actualización**: 16 de noviembre de 2025
