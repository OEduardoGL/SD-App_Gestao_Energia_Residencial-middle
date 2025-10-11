// Importa React e useState para controlar estados internos
import React, {useState} from 'react'
//constantes de config
import {APP_CONFIG} from '../utils/constants'

//componente funcional LoginForm
const LoginForm = () => {
    //estados para email e password
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    //função para lidar com o submit do formulário
    const handleSubmit = (e) => {
        e.preventDefault()
        console.log('Login attempt:', {email, password})
    }

    //Interface do form  
    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-green-100 to-emerald-200">
            <h1 className="text-4xl font-bold text-white">OLA TESTE ALOALOALO</h1>
        </div>
    )

}

//Para usar em outra arq
export default LoginForm