import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { 
  LayoutDashboard, 
  Receipt, 
  Wallet, 
  User, 
  LogOut,
  PlusCircle,
  Upload
} from 'lucide-react'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/transacoes', icon: Receipt, label: 'Transações' },
    { path: '/contas', icon: Wallet, label: 'Contas' },
    { path: '/importar', icon: Upload, label: 'Importar' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Wallet className="h-8 w-8 text-primary-600 mr-3" />
              <span className="text-xl font-bold text-gray-900">Finanças</span>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link 
                to="/transacoes/nova" 
                className="btn-primary flex items-center"
              >
                <PlusCircle className="h-4 w-4 mr-2" />
                Nova Transação
              </Link>
              
              <div className="flex items-center text-gray-600">
                <User className="h-5 w-5 mr-2" />
                <span className="text-sm">{user?.nome}</span>
              </div>
              
              <button 
                onClick={handleLogout}
                className="text-gray-500 hover:text-gray-700"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center py-4 text-sm font-medium border-b-2 transition-colors ${
                    isActive 
                      ? 'border-primary-600 text-primary-600' 
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {item.label}
                </Link>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
