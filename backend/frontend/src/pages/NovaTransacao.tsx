import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Loader2 } from 'lucide-react'
import { transacaoService } from '../services/api'
import type { TransacaoCreate } from '../types'

export default function NovaTransacao() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState<TransacaoCreate>({
    descricao: '',
    valor: 0,
    tipo: 'saida',
    categoria: 'outros',
    data: new Date().toISOString().split('T')[0],
    is_fixa: false,
    is_recorrente: false,
    observacoes: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      console.log('DEBUG: FormData sendo enviado:', formData)
      await transacaoService.createTransacao(formData)
      navigate('/transacoes')
    } catch (err: any) {
      console.log('DEBUG: Erro completo:', err)
      console.log('DEBUG: Erro response:', err.response?.data)
      setError(err.response?.data?.detail || 'Erro ao criar transação')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }))
  }

  const categorias = [
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

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center mb-6">
        <button
          onClick={() => navigate('/transacoes')}
          className="mr-4 text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Nova Transação</h1>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="card space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="label">Tipo</label>
            <select
              name="tipo"
              value={formData.tipo}
              onChange={handleChange}
              className="input"
              required
            >
              <option value="entrada">Entrada (+)</option>
              <option value="saida">Saída (-)</option>
            </select>
          </div>

          <div>
            <label className="label">Valor (R$)</label>
            <input
              type="number"
              name="valor"
              value={formData.valor}
              onChange={handleChange}
              className="input"
              step="0.01"
              min="0.01"
              required
            />
          </div>
        </div>

        <div>
          <label className="label">Descrição</label>
          <input
            type="text"
            name="descricao"
            value={formData.descricao}
            onChange={handleChange}
            className="input"
            placeholder="Ex: Supermercado, Salário, etc."
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="label">Categoria</label>
            <select
              name="categoria"
              value={formData.categoria}
              onChange={handleChange}
              className="input"
              required
            >
              {categorias.map(c => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="label">Data</label>
            <input
              type="date"
              name="data"
              value={formData.data}
              onChange={handleChange}
              className="input"
              required
            />
          </div>
        </div>

        <div className="flex space-x-6">
          <label className="flex items-center">
            <input
              type="checkbox"
              name="is_fixa"
              checked={formData.is_fixa}
              onChange={handleChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">Despesa Fixa</span>
          </label>

          <label className="flex items-center">
            <input
              type="checkbox"
              name="is_recorrente"
              checked={formData.is_recorrente}
              onChange={handleChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">Recorrente</span>
          </label>
        </div>

        <div>
          <label className="label">Observações (opcional)</label>
          <textarea
            name="observacoes"
            value={formData.observacoes}
            onChange={handleChange}
            className="input"
            rows={3}
            placeholder="Adicione observações se necessário..."
          />
        </div>

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => navigate('/transacoes')}
            className="btn-secondary flex-1"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex-1 flex items-center justify-center"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Salvando...
              </>
            ) : (
              'Salvar Transação'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
