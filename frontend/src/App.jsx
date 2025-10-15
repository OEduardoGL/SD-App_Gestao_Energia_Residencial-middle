import React from "react"
import'./App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from  './pages/Login'
import Cadastro from "./pages/Cadastro";
import Dashboard from "./pages/Dashboard";

//componnete principal da aplicação
function App() {
    return (
        // return o que será renderizado na tela
        <Router>
            <div className="App">
                <Routes>
                    <Route path='/' element={<Login />}></Route>
                    <Route path='/login' element={<Login />}></Route>
                    <Route path='/cadastro' element={<Cadastro />}></Route>
                    <Route path='/dashboard' element={<Dashboard />}></Route>
                </Routes>
            </div>
        </Router>
    )
}

//exporta componente App para que ele possa ser usado noutros arq
export default App;