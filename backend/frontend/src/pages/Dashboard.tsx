import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  AlertTriangle,
  ArrowRight,
  Loader2,
  Calendar,
  Tag
} from 'lucide-react'
import { dashboardService, transacaoService } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import type { DashboardResumo, Transacao } from '../types'

export default function Dashboard() {
  const [resumo, setResumo] = useState<DashboardResumo | null>(null)
  const [transacoes, setTransacoes] = useState<Transacao[]>([])
  const [loading, setLoading] = useState(true)
  const [gastosData, setGastosData] = useState<any[]>([])
  
  // Filtro simples por mês atual
  const [mesAno, setMesAno] = useState<string>('')
  const [categoria, setCategoria] = useState<string>('')

  useEffect(() => {
    loadDashboard()
  }, [])

  useEffect(() => {
    loadDashboard()
  }, [mesAno, categoria])

  const loadDashboard = async () => {
    try {
      const params: any = {}
      
      // Se não tiver mês selecionado, usa o mês atual
      if (mesAno) {
        const [ano, mes] = mesAno.split('-')
        params.data_inicio = `${ano}-${mes}-01`
        
        // Calcular último dia do mês corretamente
        const ultimoDia = new Date(parseInt(ano), parseInt(mes), 0).getDate()
        params.data_fim = `${ano}-${mes}-${ultimoDia.toString().padStart(2, '0')}`
      } else {
        // Mês atual por padrão
        const hoje = new Date()
        const inicioMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1).toISOString().split('T')[0]
        const fimMes = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0).toISOString().split('T')[0]
        params.data_inicio = inicioMes
        params.data_fim = fimMes
      }

      // Adicionar filtro de categoria
      if (categoria) {
        params.categoria = categoria
      }

      // Carregar transações filtradas
      const transacoesData = await transacaoService.getTransacoes(params)
      setTransacoes(transacoesData)
      
      // Calcular resumo baseado nas transações filtradas
      const totalEntradas = transacoesData
        .filter((t: Transacao) => t.tipo === 'entrada')
        .reduce((sum: number, t: Transacao) => sum + Number(t.valor), 0)
      
      const totalSaidas = transacoesData
        .filter((t: Transacao) => t.tipo === 'saida')
        .reduce((sum: number, t: Transacao) => sum + Number(t.valor), 0)
      
      const balanco = totalEntradas - totalSaidas
      
      // Calcular saldo (soma de todas as transações até a data final)
      let saldo = 0
      transacoesData.forEach((t: Transacao) => {
        if (t.tipo === 'entrada') saldo += Number(t.valor)
        else saldo -= Number(t.valor)
      })
      
      setResumo({
        saldo_atual: saldo,
        total_entradas_mes: totalEntradas,
        total_saidas_mes: totalSaidas,
        balanco_mes: balanco,
        transacoes_recentes: transacoesData.slice(0, 5),
        alertas_orcamento: []
      })
      
      // Preparar dados para o gráfico
      const gastos = transacoesData
        .filter((t: Transacao) => t.tipo === 'saida')
        .reduce((acc: any, t: Transacao) => {
          acc[t.categoria] = (acc[t.categoria] || 0) + Number(t.valor)
          return acc
        }, {})
      
      const chartData = Object.entries(gastos).map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        value
      }))
      setGastosData(chartData)
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384']

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    )
  }

  if (!resumo) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Erro ao carregar dados do dashboard</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        
        {/* Filtros */}
        <div className="flex items-center space-x-4">
          {/* Filtro de Mês/Ano */}
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-400" />
            <input
              type="month"
              value={mesAno}
              onChange={(e) => setMesAno(e.target.value)}
              className="input w-40"
              placeholder="Mês/Ano"
            />
          </div>
          
          {/* Filtro de Categoria */}
          <div className="flex items-center space-x-2">
            <Tag className="h-4 w-4 text-gray-400" />
            <select
              value={categoria}
              onChange={(e) => setCategoria(e.target.value)}
              className="input w-40"
            >
              <option value="">Todas</option>
              <option value="alimentacao">Alimentação</option>
              <option value="transporte">Transporte</option>
              <option value="moradia">Moradia</option>
              <option value="saude">Saúde</option>
              <option value="lazer">Lazer</option>
              <option value="educacao">Educação</option>
              <option value="outros">Outros</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Saldo Atual</p>
              <p className={`text-2xl font-bold ${resumo.saldo_atual >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(resumo.saldo_atual)}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Entradas do Mês</p>
              <p className="text-2xl font-bold text-green-600">
                {formatCurrency(resumo.total_entradas_mes)}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-red-100 rounded-lg">
              <TrendingDown className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Saídas do Mês</p>
              <p className="text-2xl font-bold text-red-600">
                {formatCurrency(resumo.total_saidas_mes)}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Balanço</p>
              <p className={`text-2xl font-bold ${resumo.balanco_mes >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(resumo.balanco_mes)}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de Gastos */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Gastos por Categoria</h2>
          {gastosData.length > 0 ? (
            <div className="flex justify-center">
              <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                  <Pie
                    data={gastosData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {gastosData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: number) => formatCurrency(value)} />
                  <Legend 
                    verticalAlign="bottom" 
                    height={36}
                    formatter={(value) => <span className="text-sm">{value}</span>}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex items-center justify-center h-80 text-gray-500">
              Sem dados de gastos para este período
            </div>
          )}
        </div>

        {/* Transações Recentes */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              {mesAno ? `Transações de ${new Date(mesAno + '-01').toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })}` : 'Transações do Mês'}
              {categoria && ` - ${categoria.charAt(0).toUpperCase() + categoria.slice(1)}`}
            </h2>
            <Link to="/transacoes" className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center">
              Ver todas
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
          
          {transacoes?.length > 0 ? (
            <div className="space-y-3">
              {transacoes.slice(0, 5).map((transacao) => (
                <div key={transacao.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{transacao.descricao}</p>
                    <p className="text-sm text-gray-500">{formatDate(transacao.data)}</p>
                  </div>
                  <p className={`font-semibold ${transacao.tipo === 'entrada' ? 'text-green-600' : 'text-red-600'}`}>
                    {transacao.tipo === 'entrada' ? '+' : '-'}{formatCurrency(Number(transacao.valor))}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              {mesAno 
                ? 'Nenhuma transação neste mês' 
                : 'Nenhuma transação registrada'}
            </p>
          )}
        </div>
      </div>

      {/* Alertas de Orçamento */}
      {resumo.alertas_orcamento && resumo.alertas_orcamento.length > 0 && (
        <div className="card border-l-4 border-yellow-400">
          <div className="flex items-center mb-4">
            <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Alertas de Orçamento</h2>
          </div>
          <div className="space-y-2">
            {resumo.alertas_orcamento.map((alerta, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                <span className="font-medium text-gray-900 capitalize">{alerta.categoria}</span>
                <div className="text-right">
                  <p className="text-sm text-gray-600">
                    {formatCurrency(alerta.gasto_real)} de {formatCurrency(alerta.orcado)}
                  </p>
                  <p className={`text-sm font-semibold ${alerta.percentual_usado > 90 ? 'text-red-600' : 'text-yellow-600'}`}>
                    {alerta.percentual_usado}% utilizado
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
