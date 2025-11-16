# 🎨 URLytics Web - Frontend React

Aplicación web moderna de URLytics con background 3D interactivo y sistema de detección de phishing impulsado por IA.

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Node.js >= 18.0.0
- npm >= 9.0.0
- API Flask corriendo en `http://localhost:5000`

### Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Abrir en navegador: http://localhost:5173
```

### Comandos Disponibles

```bash
npm run dev      # Servidor de desarrollo con HMR
npm run build    # Build de producción en /dist
npm run preview  # Preview del build de producción
```

---

## 📦 Stack Tecnológico

- **React 18.3** - Framework UI
- **Vite 5.4** - Build tool y dev server
- **Tailwind CSS 3.4** - Estilos utility-first
- **Three.js** - Renderizado 3D del background
- **shadcn/ui** - Componentes UI reutilizables

---

## 🎨 Características

### ✨ Background Interactivo 3D
- Distorsión de malla reactiva al mouse
- Texturas SVG dinámicas
- Gradientes multicapa con blend modes

### 🌓 Theming Dark/Light
- **Modo Oscuro**: Rosa/Fucsia/Magenta
- **Modo Claro**: Negro/Azul/Cyan
- Persistencia en localStorage

### 🛡️ Análisis de Phishing
- Entrada de texto/URL
- Validación en tiempo real
- Visualización de resultados con colores
- Indicadores de nivel de riesgo

### 📱 Responsive Design
- Mobile-first approach
- Breakpoints adaptivos
- Card centrado con glassmorphism

---

## 🔌 Integración con API

La aplicación se conecta automáticamente a la API Flask de URLytics:

```javascript
// Endpoint de predicción
POST http://localhost:5000/predict
Content-Type: application/json
Body: { "text": "URL o texto a analizar" }
```

**Asegúrate de iniciar el backend antes:**

```bash
cd "/home/huaritex/Desktop/social engineer"
python api.py
```

---

## 📂 Estructura del Proyecto

```
urlytics-web/
├── src/
│   ├── App.jsx              # Componente principal
│   ├── main.jsx             # Entry point
│   ├── components/
│   │   ├── GridDistortion.jsx  # Background 3D
│   │   └── ui/              # shadcn components
│   └── lib/
│       └── utils.js         # Utilities
├── public/                  # Assets estáticos
├── dist/                    # Build output
└── package.json             # Dependencias
```

---

## 🎯 Uso

1. **Activa URLytics**: Toggle en el header
2. **Ingresa texto**: URL o mensaje sospechoso
3. **Analizar**: Click en "Analizar Texto"
4. **Revisa resultados**: Nivel de riesgo y confianza

---

## 🐛 Troubleshooting

### El servidor no inicia

```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Error de conexión con API

1. Verifica que Flask esté corriendo:
   ```bash
   curl http://localhost:5000/health
   ```

2. Revisa CORS en `api.py`:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

### Background no se renderiza

1. Verifica instalación de Three.js:
   ```bash
   npm list three
   ```

2. Revisa consola del navegador para errores WebGL

---

## 📚 Documentación Completa

- **[FRONTEND_REACT.md](../docs/frontend/FRONTEND_REACT.md)** - Documentación técnica detallada
- **[INTEGRACION_API.md](../docs/api/INTEGRACION_API.md)** - Guía de integración con backend

---

## 🏗️ Build de Producción

```bash
# Generar build
npm run build

# Output en /dist:
# - index.html (0.58 kB)
# - assets/index-*.css (21 kB)
# - assets/index-*.js (641 kB)

# Servir build
npm run preview
```

---

## 🔧 Configuración

### Vite (`vite.config.js`)

```javascript
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") }
  }
})
```

### Tailwind (`tailwind.config.js`)

```javascript
module.exports = {
  darkMode: ["class"],
  content: ["./src/**/*.{js,jsx}"],
  // ...
}
```

---

## 👨‍💻 Desarrollo

### Añadir nuevos componentes

```bash
# Usar shadcn CLI
npx shadcn@latest add [component-name]
```

### Hot Module Replacement (HMR)

Vite proporciona HMR automático. Los cambios en `src/` se reflejan instantáneamente.

---

## 📊 Rendimiento

- **Build Time**: ~2.3s
- **Dev Server**: ~160ms startup
- **Bundle Size**: 641 kB (175 kB gzipped)

---

## 🚀 Próximos Pasos

- [ ] Implementar PWA
- [ ] Añadir tests (Vitest)
- [ ] Code splitting para Three.js
- [ ] Internacionalización (i18n)

---

## 📄 Licencia

Parte de URLytics v2.3 - Sistema de detección de phishing

**By Huaritex** | Noviembre 2025
