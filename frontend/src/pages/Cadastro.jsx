import React, { useState } from 'react'
import { APP_CONFIG } from '../utils/constants'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

const Cadastro = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    senha: '',
    confirmarSenha: ''})
      
  const handleSubmit = (e) => {
    e.preventDefault()
    //validação
    console.log('Cadastro attempt:', { 
      nome: formData.nome, 
      email: formData.email, 
      senha: formData.senha, 
      confirmarSenha: formData.confirmarSenha 
    })
    //vai pra dashboard
    navigate('/dashboard')
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        {/* logo */}
            <div className="text-center mb-8">
                <div className="flex justify-center mb-4">
                    <img 
                        src="/images/logo.png" 
                        alt="Voltix" 
                        className="h-20 w-20" 
                    />
            </div>

          <p className="text-gray-600 text-sm">
            {APP_CONFIG.description}
          </p>
        </div>

        {/*Menssagem de boas vindas*/}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 text-center">
            Crie sua conta
          </h2>
          <p className="text-gray-600 text-sm text-center mt-2">
            Comece a monitorar seu consumo de energia.
          </p>
        </div>

        <div className="w-12 h-1 bg-gradient-to-r from-green-500 to-green-600 mx-auto mb-8 rounded-full"></div>

        {/*cadastro*/}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/*nome completo*/}
          <div>
            <label className="flex items-center text-sm font-medium text-gray-700 mb-3">
              <div className="w-4 h-4 border-2 border-gray-300 rounded mr-3 flex items-center justify-center">
                <div className="w-2 h-2 bg-green-500 rounded-sm"></div>
              </div>
              Nome Completo
            </label>
            <input
              type="text"
              name="nome"
              value={formData.nome}
              onChange={handleChange}
              placeholder="Seu nome completo"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all"
              required
            />
          </div>

          {/*emaill */}
          <div>
            <label className="flex items-center text-sm font-medium text-gray-700 mb-3">
              <div className="w-4 h-4 border-2 border-gray-300 rounded mr-3 flex items-center justify-center">
                <div className="w-2 h-2 bg-green-500 rounded-sm"></div>
              </div>
              Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="seu@email.com"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all"
              required
            />
          </div>

          {/* senha */}
          <div>
            <label className="flex items-center text-sm font-medium text-gray-700 mb-3">
              <div className="w-4 h-4 border-2 border-gray-300 rounded mr-3 flex items-center justify-center">
                <div className="w-2 h-2 bg-green-500 rounded-sm"></div>
              </div>
              Senha
            </label>
            <div className="relative">
              <input
                type="password"
                name="senha"
                value={formData.senha}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all pr-12"
                required
              />
              <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
                <div className="flex space-x-1">
                </div>
              </div>
            </div>
          </div>

          {/* confirmação de senha */}
          <div>
            <label className="flex items-center text-sm font-medium text-gray-700 mb-3">
              <div className="w-4 h-4 border-2 border-gray-300 rounded mr-3 flex items-center justify-center">
                <div className="w-2 h-2 bg-green-500 rounded-sm"></div>
              </div>
              Confirmar Senha
            </label>
            <div className="relative">
              <input
                type="password"
                name="confirmarSenha"
                value={formData.confirmarSenha}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all pr-12"
                required
              />
              <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
                <div className="flex space-x-1">
                </div>
              </div>
            </div>
          </div>

          {/*btao de cadastrar*/}
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-4 rounded-lg font-semibold hover:from-green-600 hover:to-green-700 focus:ring-2 focus:ring-green-300 focus:ring-offset-2 transition-all transform hover:-translate-y-0.5"
          >
            Cadastrar
          </button>
        </form>

        {/*link de login*/}
        <div className="text-center mt-6">
          <p className="text-gray-600 text-sm">
            Já tem uma conta?{' '}
            <Link to='/login' className="text-green-500 font-semibold hover:text-green-600 transition-colors">
            Faça login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Cadastro