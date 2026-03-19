import { useState, useEffect } from 'react'
import { Plus, Trash2, Loader2, Building2 } from 'lucide-react'
import { contaService } from '../services/api'
import type { ContaBancaria } from '../types'

export default function Contas() {
  const [contas, setContas] = useState<ContaBancaria[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [novaConta, setNovaConta] = useState({
    nome_banco: '',
    agencia: '',
    conta: '',
    tipo_conta: '',
    saldo: 0
  })

  useEffect(() => {
    loadContas()
  }, [])

  const loadContas = async () => {
    try {
      const data = await contaService.getContas()
      setContas(data)
    } catch (error) {
      console.error('Erro ao carregar contas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await contaService.createConta(novaConta)
      setNovaConta({ nome_banco: '', agencia: '', conta: '', tipo_conta: '', saldo: 0 })
      setShowForm(false)
      loadContas()
    } catch (error) {
      console.error('Erro ao criar conta:', error)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Tem certeza que deseja remover esta conta?')) return
    
    try {
      await contaService.deleteConta(id)
      setContas(contas.filter(c => c.id !== id))
    } catch (error) {
      console.error('Erro ao remover conta:', error)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

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
        <h1 className="text-2xl font-bold text-gray-900">Contas Bancárias</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center"
        >
          <Plus className="h-4 w-4 mr-2" />
          {showForm ? 'Cancelar' : 'Nova Conta'}
        </button>
      </div>

      {/* Formulário */}
      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="label">Nome do Banco</label>
              <input
                type="text"
                value={novaConta.nome_banco}
                onChange={(e) => setNovaConta({...novaConta, nome_banco: e.target.value})}
                className="input"
                placeholder="Ex: Banco do Brasil"
                required
              />
            </div>
            <div>
              <label className="label">Tipo de Conta</label>
              <select
                value={novaConta.tipo_conta}
                onChange={(e) => setNovaConta({...novaConta, tipo_conta: e.target.value})}
                className="input"
              >
                <option value="">Selecione...</option>
                <option value="corrente">Conta Corrente</option>
                <option value="poupanca">Poupança</option>
                <option value="investimento">Investimento</option>
                <option value="cartao">Cartão de Crédito</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="label">Agência</label>
              <input
                type="text"
                value={novaConta.agencia}
                onChange={(e) => setNovaConta({...novaConta, agencia: e.target.value})}
                className="input"
                placeholder="0000"
              />
            </div>
            <div>
              <label className="label">Conta</label>
              <input
                type="text"
                value={novaConta.conta}
                onChange={(e) => setNovaConta({...novaConta, conta: e.target.value})}
                className="input"
                placeholder="00000-0"
              />
            </div>
            <div>
              <label className="label">Saldo Inicial</label>
              <input
                type="number"
                value={novaConta.saldo}
                onChange={(e) => setNovaConta({...novaConta, saldo: Number(e.target.value)})}
                className="input"
                step="0.01"
              />
            </div>
          </div>
          <button type="submit" className="btn-primary w-full md:w-auto">
            Cadastrar Conta
          </button>
        </form>
      )}

      {/* Lista de Contas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {contas.length === 0 ? (
          <div className="col-span-full card text-center py-12 text-gray-500">
            <Building2 className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p>Nenhuma conta cadastrada</p>
          </div>
        ) : (
          contas.map((conta) => (
            <div key={conta.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex items-center">
                  <div className="p-3 bg-primary-100 rounded-lg">
                    <Building2 className="h-5 w-5 text-primary-600" />
                  </div>
                  <div className="ml-3">
                    <h3 className="font-semibold text-gray-900">{conta.nome_banco}</h3>
                    <p className="text-sm text-gray-500 capitalize">{conta.tipo_conta || 'Conta'}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(conta.id)}
                  className="text-gray-400 hover:text-red-600"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  Agência: {conta.agencia || '-'}
                </p>
                <p className="text-sm text-gray-600">
                  Conta: {conta.conta || '-'}
                </p>
                <p className="text-xl font-bold mt-3 text-gray-900">
                  {formatCurrency(Number(conta.saldo))}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
