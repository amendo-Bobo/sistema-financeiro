import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Edit2, Trash2, Loader2, Search, Calendar } from 'lucide-react'
import { transacaoService } from '../services/api'
import type { Transacao } from '../types'

export default function Transacoes() {
  const [transacoes, setTransacoes] = useState<Transacao[]>([])
  const [loading, setLoading] = useState(true)
  const [filtroTipo, setFiltroTipo] = useState<string>('')
  const [filtroCategoria, setFiltroCategoria] = useState<string>('')
  const [dataInicio, setDataInicio] = useState<string>('')
  const [dataFim, setDataFim] = useState<string>('')

  useEffect(() => {
    loadTransacoes()
  }, [filtroTipo, filtroCategoria, dataInicio, dataFim])

  const loadTransacoes = async () => {
    try {
      const params: any = {}
      if (filtroTipo) params.tipo = filtroTipo
      if (filtroCategoria) params.categoria = filtroCategoria
      if (dataInicio) params.data_inicio = dataInicio
      if (dataFim) params.data_fim = dataFim
      
      const data = await transacaoService.getTransacoes(params)
      setTransacoes(data)
    } catch (error) {
      console.error('Erro ao carregar transações:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Tem certeza que deseja excluir esta transação?')) return
    
    try {
      await transacaoService.deleteTransacao(id)
      setTransacoes(transacoes.filter(t => t.id !== id))
    } catch (error) {
      console.error('Erro ao excluir transação:', error)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  const categorias = [
    { value: '', label: 'Todas' },
    { value: 'alimentacao', label: 'Alimentação' },
    { value: 'transporte', label: 'Transporte' },
    { value: 'moradia', label: 'Moradia' },
    { value: 'saude', label: 'Saúde' },
    { value: 'educacao', label: 'Educação' },
    { value: 'lazer', label: 'Lazer' },
    { value: 'vestuario', label: 'Vestuário' },
    { value: 'utilidades', label: 'Utilidades' },
    { value: 'salario', label: 'Salário' },
    { value: 'investimentos', label: 'Investimentos' },
    { value: 'outros', label: 'Outros' },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Transações</h1>
        <Link to="/transacoes/nova" className="btn-primary flex items-center">
          <Plus className="h-4 w-4 mr-2" />
          Nova Transação
        </Link>
      </div>

      {/* Filtros */}
      <div className="card flex flex-wrap gap-4">
        <div className="flex items-center space-x-2">
          <Search className="h-4 w-4 text-gray-400" />
          <select
            value={filtroTipo}
            onChange={(e) => setFiltroTipo(e.target.value)}
            className="input w-40"
          >
            <option value="">Todos os tipos</option>
            <option value="entrada">Entrada</option>
            <option value="saida">Saída</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <select
            value={filtroCategoria}
            onChange={(e) => setFiltroCategoria(e.target.value)}
            className="input w-48"
          >
            {categorias.map(c => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <Calendar className="h-4 w-4 text-gray-400" />
          <input
            type="date"
            value={dataInicio}
            onChange={(e) => setDataInicio(e.target.value)}
            className="input w-40"
            placeholder="Data início"
          />
          <span className="text-gray-400">até</span>
          <input
            type="date"
            value={dataFim}
            onChange={(e) => setDataFim(e.target.value)}
            className="input w-40"
            placeholder="Data fim"
          />
        </div>
      </div>

      {/* Tabela */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descrição
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoria
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transacoes.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                    Nenhuma transação encontrada
                  </td>
                </tr>
              ) : (
                transacoes.map((transacao) => (
                  <tr key={transacao.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(transacao.data)}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {transacao.descricao}
                      {transacao.is_fixa && (
                        <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          Fixa
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 capitalize">
                      {transacao.categoria}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium text-right ${
                      transacao.tipo === 'entrada' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {transacao.tipo === 'entrada' ? '+' : '-'}
                      {formatCurrency(Number(transacao.valor))}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                      <button
                        onClick={() => handleDelete(transacao.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
