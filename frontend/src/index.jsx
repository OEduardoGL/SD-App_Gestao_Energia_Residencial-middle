import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/global.css'

// Cria raiz da app react no HTML com id root
ReactDOM.createRoot(document.getElementById('root')).render(
  //  Ajuda a identificar probelmas na aplicação
  <React.StrictMode>
    {/* Renderiza o componente principal da aplicação*/}
    <App />
  </React.StrictMode>
)