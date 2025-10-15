import React from 'react'
import { Link } from 'react-router-dom'

const DashboardLayout = ({ children }) => {
    return (
        <div className='flex h-screen bg-gray-50'>
            {/*a sidebar*/}
            <div className='w-64 bg-white shadow-lg'>
                <div className='p-6'>
                    <h1 className='text-2xl font-bold text-primary-600'>VOLTIX</h1>
                    <p className='text-sm text-gray-600'>Gestão Inteligente de Energia</p>
                </div>
                
                <nav className='mt-6'>
                    {[
                        { name: 'Dashboard', icon: '', active: true},
                        { name: 'Relatórios'}
                    ]}
                </nav>

            </div>
        </div>
    )
}

export default DashboardLayout