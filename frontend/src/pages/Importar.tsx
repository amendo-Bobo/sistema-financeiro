import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, CheckCircle, AlertCircle, Loader2, Building2 } from 'lucide-react'
import { importacaoService } from '../services/api'
import type { Transacao } from '../types'

export default function Importar() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null)
  const [banco, setBanco] = useState('auto')
  const [loading, setLoading] = useState(false)
  const [resultado, setResultado] = useState<{
    sucesso: Transacao[]
    erro: string | null
  } | null>(null)

  const bancos = [
    { id: 'auto', nome: 'Detectar automaticamente' },
    { id: 'mercado_pago', nome: 'Mercado Pago' },
    { id: 'nubank', nome: 'Nubank' },
    { id: 'itau', nome: 'Itaú' },
    { id: 'bradesco', nome: 'Bradesco' },
    { id: 'santander', nome: 'Santander' },
    { id: 'bb', nome: 'Banco do Brasil' },
    { id: 'caixa', nome: 'Caixa Econômica' },
    { id: 'inter', nome: 'Banco Inter' },
    { id: 'c6', nome: 'C6 Bank' },
    { id: 'original', nome: 'Banco Original' },
    { id: 'generico', nome: 'Outros/Genérico' },
  ]

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setResultado(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)
    setResultado(null)

    try {
      const transacoes = await importacaoService.importarArquivo(file, banco)
      setResultado({
        sucesso: transacoes,
        erro: null
      })
      setFile(null)
      
      // Redirecionar para transações após 2 segundos se importação foi bem-sucedida
      if (transacoes.length > 0) {
        setTimeout(() => {
          navigate('/transacoes')
        }, 2000)
      }
    } catch (err: any) {
      setResultado({
        sucesso: [],
        erro: err.response?.data?.detail || 'Erro ao importar arquivo'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Importar Extrato Bancário</h1>

      <div className="card mb-6">
        <div className="flex items-center text-blue-600 mb-4">
          <Building2 className="h-5 w-5 mr-2" />
          <span className="font-medium">Sem custo e sem burocracia!</span>
        </div>
        <p className="text-sm text-gray-600">
          Importe seu extrato diretamente do Internet Banking ou apps. Suportamos arquivos <strong>OFX</strong> (padrão), <strong>CSV</strong> e <strong>PDF</strong> dos principais bancos.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-6">
        {/* Seleção de banco */}
        <div>
          <label className="label flex items-center">
            <Building2 className="h-4 w-4 mr-2" />
            Banco
          </label>
          <select
            value={banco}
            onChange={(e) => setBanco(e.target.value)}
            className="input"
          >
            {bancos.map(b => (
              <option key={b.id} value={b.id}>{b.nome}</option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Selecione seu banco ou deixe em "Detectar automaticamente"
          </p>
        </div>

        {/* Upload de arquivo */}
        <div>
          <label className="label flex items-center">
            <FileText className="h-4 w-4 mr-2" />
            Arquivo do Extrato
          </label>
          
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors">
            <input
              type="file"
              accept=".ofx,.qfx,.csv,.txt,.pdf,.xlsx,.xls"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center"
            >
              <Upload className="h-10 w-10 text-gray-400 mb-3" />
              <span className="text-gray-600 font-medium">
                {file ? file.name : 'Clique para selecionar arquivo'}
              </span>
              <span className="text-sm text-gray-400 mt-1">
                OFX, QFX, CSV, XLSX ou PDF (até 10MB)
              </span>
            </label>
          </div>
        </div>

        {/* Botão de importar */}
        <button
          type="submit"
          disabled={!file || loading}
          className="btn-primary w-full flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              Importando...
            </>
          ) : (
            <>
              <Upload className="h-4 w-4 mr-2" />
              Importar Transações
            </>
          )}
        </button>
      </form>

      {/* Resultado */}
      {resultado && (
        <div className={`card mt-6 ${resultado.erro ? 'border-red-200' : 'border-green-200'}`}>
          {resultado.erro ? (
            <div className="flex items-start text-red-700">
              <AlertCircle className="h-5 w-5 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium">Erro na importação</p>
                <p className="text-sm mt-1">{resultado.erro}</p>
              </div>
            </div>
          ) : (
            <div>
              <div className="flex items-center text-green-700 mb-4">
                <CheckCircle className="h-5 w-5 mr-2" />
                <span className="font-medium">
                  {resultado.sucesso.length} transação(ões) importada(s) com sucesso!
                </span>
              </div>
              
              {resultado.sucesso.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Transações importadas:</h3>
                  <div className="max-h-64 overflow-y-auto space-y-2">
                    {resultado.sucesso.map((t, i) => (
                      <div key={i} className="bg-gray-50 p-3 rounded text-sm">
                        <div className="flex justify-between">
                          <span className="font-medium text-gray-900">{t.descricao}</span>
                          <span className={t.tipo === 'entrada' ? 'text-green-600' : 'text-red-600'}>
                            R$ {t.valor.toFixed(2)}
                          </span>
                        </div>
                        <div className="text-gray-500 text-xs mt-1">
                          {new Date(t.data).toLocaleDateString('pt-BR')} • {t.categoria}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Instruções */}
      <div className="card mt-6 bg-gray-50">
        <h3 className="font-medium text-gray-900 mb-3">Como obter seu extrato:</h3>
        <ul className="text-sm text-gray-600 space-y-2">
          <li>• <strong>Mercado Pago:</strong> App → Extrato → Exportar → CSV, XLSX ou PDF</li>
          <li>• <strong>Nubank:</strong> App → Extrato → Compartilhar → CSV</li>
          <li>• <strong>Itaú:</strong> Internet Banking → Extrato → Exportar OFX</li>
          <li>• <strong>Bradesco:</strong> Extrato → Exportar → OFX/CSV</li>
          <li>• <strong>Inter:</strong> Extrato → Download → CSV</li>
          <li>• <strong>Outros:</strong> Procure "Exportar" ou "Download" no extrato</li>
        </ul>
      </div>
    </div>
  )
}
