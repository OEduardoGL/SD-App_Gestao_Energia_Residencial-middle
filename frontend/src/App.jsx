import React from "react"
import Login from  './pages/Login'
import'./App.css'

//componnete principal da aplicação
function App() {
    return (
        // return o que será renderizado na tela
        <div className="App">
            <Login />
        </div>
    )
}

//exporta componente App para que ele possa ser usado noutros arq
export default App;