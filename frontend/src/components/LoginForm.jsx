// Importa React e useState para controlar estados internos
import React, {useState} from 'react'
//constantes de config
import {APP_CONFIG} from '../utils/constants'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

//componente funcional LoginForm
const LoginForm = () => {
    const navigate = useNavigate()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    
    const handleSubmit = (e) => {
        e.preventDefault()
        //validação
        console.log('Login attempt:', { email, password })
        
        //vai pra dashboard
        navigate('/dashboard')
    }

    //Interface do form  
    return (
        <div className="min-h-screen flex items-center justify-center p-4 gradient-bg">
           
            <div className="bg-white rounded-2xl shadow-2xl p-10 max-w-md w-full">
                {/* logo */}
                <div className="text-center mb-8">
                    <div className="flex justify-center mb-4">
                        <img 
                            src="/images/logo.png" 
                            alt="Voltix" 
                            className="h-20 w-20" 
                        />
                    </div>
                    
                    <p className='text-gray-600 text-lg font-medium'>
                        {APP_CONFIG.description}
                    </p>
                </div>

            {/*Menssagem de boas vindas*/}
            <div className='mb-8'>
                <h2 className='text-xl font-semibold text-gray-900 text-center'>
                    {APP_CONFIG.welcomeMessage}
                </h2>

                <p className='text-gray-600 text-sm text-center mt-2'>
                    {APP_CONFIG.loginMessage}
                </p>
            </div>

            <div className='w-12 h-1 bg-gradient-to-r from-green-300 to-green-600 mx-auto mb-8 rounded-full'></div>
           
           {/*Formulario*/}
           <form onSubmit={handleSubmit} className='space-y-6'>
                {/*Campo de email*/}
                <div>
                    <label className='flex items-center text-sm font-medium text-gray-700 mb3'>
                        <div className='w-4 h-4 border-2 border-gray-300 rounded mr-3 flex items-center justify-center'>
                            <div className='w-2 h-2 bg-green-500 rounded-sm'></div> 
                        </div>
                        Email
                    </label>
                    <input 
                    type='email' 
                    value={email} 
                    onChange={(e) =>setEmail(e.target.value)}
                    placeholder='seu@email.com'
                    className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all'
                    required>
                    </input>
                </div>

                {/*Campo de senha*/}
                <div>
                    <label className='flex items-center text-sm font-medium text-gray-700 mb3'>
                        <div className='w-4 h-4 border-2 border-gray-300 rounded mr-3 flex items-center justify-center'>
                            <div className='w-2 h-2 bg-green-500 rounded-sm'></div>
                        </div>
                        Senha
                    </label>
                    <div className='relative'>
                        <input
                        type='password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder='********'
                        className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all pr-12'
                        required>
                        </input>
                        <div className='absolute right-4 top-1/2 transform -translate-y-1/2'>
                            <div className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all'>
                            </div>
                        </div>
                    </div>
                </div>

                {/*Botão de login*/}
                <button
                type='submit'
                className='w-full bg-gradient-to-r from-green-400 to-green-600 text-white px-4 py-3 rounded-lg font-semibold hover:from-green-500 hover:to-green-700 focus:ring-2 focus:ring-green-300 focus:ring-offset-2 transition-all transform hover:-translate-y-0.5'>
                    Entrar
                </button>
           </form>

            {/*Rodapé*/}
                <div className='text-center mt-6'>
                        <p className='text-sm text-gray-600'>
                            {APP_CONFIG.noAcesseMessage}{' '}
                            <Link to='/cadastro' className='text-green-500 font-semibold hover:text-green-600 transition-colors'>
                            Cadastre-se
                            </Link>
                        </p>
                </div>
            </div>
        </div>
    )
}

export default LoginForm