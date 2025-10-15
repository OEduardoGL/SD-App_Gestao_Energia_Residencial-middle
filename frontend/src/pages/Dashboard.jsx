import React from 'react'
import DashboardLayout from '../components/DashboardLayout'

const Dashboard = () => {
  return (
    <DashboardLayout>
      <div className="p-6">
        <h1 className="text-2xl font-bold text-green-600">
          ✅ Dashboard Funcionando!
        </h1>
        <p className="text-gray-600 mt-2">
          Rotas estão funcionando! Você pode voltar ao Login ou Cadastro.
        </p>
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <p>Componentes do dashboard serão adicionados amanhã.</p>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Dashboard