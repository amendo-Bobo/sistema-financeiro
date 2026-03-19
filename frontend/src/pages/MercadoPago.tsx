import { useState, useEffect } from 'react'
import { CreditCard, Key, RefreshCw, CheckCircle, AlertCircle, Loader2, HelpCircle, ExternalLink } from 'lucide-react'
import { mercadoPagoService } from '../services/api'
import type { Transacao } from '../types'

export default function MercadoPago() {
  const [accessToken, setAccessToken] = useState('')
  const [loading, setLoading] = useState(false)
  const [syncing, setSyncing] = useState(false)
  const [instrucoes, setInstrucoes] = useState<any>(null)
  const [testResult, setTestResult] = useState<any>(null)
  const [resultado, setResultado] = useState<{
    sucesso: Transacao[]
    erro: string | null
  } | null>(null)
  const [days, setDays] = useState(30)

  useEffect(() => {
    loadInstrucoes()
  }, [])

  const loadInstrucoes = async () => {
    try {
      const data = await mercadoPagoService.getInstrucoes()
      setInstrucoes(data)
    } catch (error) {
      console.error('Erro ao carregar instruções:', error)
    }
  }

  const handleTestToken = async () => {
    if (!accessToken.trim()) return

    setLoading(true)
    setTestResult(null)

    try {
      const result = await mercadoPagoService.testarToken(accessToken)
      setTestResult(result)
    } catch (err: any) {
      setTestResult({
        valid: false,
        message: err.response?.data?.detail || 'Erro ao testar token'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSync = async () => {
    if (!accessToken.trim()) return

    setSyncing(true)
    setResultado(null)

    try {
      const transacoes = await mercadoPagoService.sincronizar(accessToken, days)
      setResultado({
        sucesso: transacoes,
        erro: null
      })
    } catch (err: any) {
      setResultado({
        sucesso: [],
        erro: err.response?.data?.detail || 'Erro ao sincronizar'
      })
    } finally {
      setSyncing(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
        <CreditCard className="h-6 w-6 mr-2 text-primary-600" />
        Integração Mercado Pago
      </h1>

      <div className="card mb-6 bg-blue-50">
        <div className="flex items-start">
          <HelpCircle className="h-5 w-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="font-medium text-blue-900">Como funciona?</h3>
            <p className="text-sm text-blue-700 mt-1">
              Conecte sua conta Mercado Pago usando um <strong>Access Token</strong> pessoal. 
              Isso permite sincronizar automaticamente seus pagamentos, transferências Pix e 
              movimentações sem precisar baixar arquivos manualmente.
            </p>
            <p className="text-sm text-blue-700 mt-2">
              <strong>Segurança:</strong> O token é usado apenas para ler seus dados e nunca 
              é armazenado permanentemente. Você pode revogá-lo a qualquer momento no site do Mercado Pago.
            </p>
          </div>
        </div>
      </div>

      {/* Configuração do Token */}
      <div className="card space-y-6">
        <div>
          <label className="label flex items-center">
            <Key className="h-4 w-4 mr-2" />
            Access Token do Mercado Pago
          </label>
          <input
            type="password"
            value={accessToken}
            onChange={(e) => setAccessToken(e.target.value)}
            className="input"
            placeholder="TEST-0000000000000000-000000... ou APP_USR-..."
          />
          <p className="text-xs text-gray-500 mt-1">
            Cole aqui o Access Token obtido na aba "Credenciais de produção" da sua aplicação no Mercado Pago Developers
          </p>
        </div>

        {/* Período de sincronização */}
        <div>
          <label className="label">Período de sincronização</label>
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="input"
          >
            <option value={7}>Últimos 7 dias</option>
            <option value={30}>Últimos 30 dias</option>
            <option value={60}>Últimos 60 dias</option>
            <option value={90}>Últimos 90 dias</option>
          </select>
        </div>

        {/* Botões */}
        <div className="flex space-x-4">
          <button
            onClick={handleTestToken}
            disabled={!accessToken || loading}
            className="btn-secondary flex-1 flex items-center justify-center"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Testando...
              </>
            ) : (
              <>
                <CheckCircle className="h-4 w-4 mr-2" />
                Testar Token
              </>
            )}
          </button>

          <button
            onClick={handleSync}
            disabled={!accessToken || syncing || (testResult && !testResult.valid)}
            className="btn-primary flex-1 flex items-center justify-center"
          >
            {syncing ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Sincronizando...
              </>
            ) : (
              <>
                <RefreshCw className="h-4 w-4 mr-2" />
                Sincronizar
              </>
            )}
          </button>
        </div>

        {/* Resultado do teste */}
        {testResult && (
          <div className={`p-4 rounded-lg ${testResult.valid ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
            <div className="flex items-start">
              {testResult.valid ? (
                <CheckCircle className="h-5 w-5 text-green-600 mr-3 flex-shrink-0" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0" />
              )}
              <div>
                <p className={`font-medium ${testResult.valid ? 'text-green-900' : 'text-red-900'}`}>
                  {testResult.valid ? 'Token válido!' : 'Token inválido'}
                </p>
                <p className={`text-sm mt-1 ${testResult.valid ? 'text-green-700' : 'text-red-700'}`}>
                  {testResult.message}
                </p>
                {testResult.valid && testResult.balance && (
                  <div className="mt-3 text-sm text-green-700">
                    <p><strong>Saldo total:</strong> R$ {testResult.balance.total?.toFixed(2) || '0.00'}</p>
                    <p><strong>Disponível:</strong> R$ {testResult.balance.disponivel?.toFixed(2) || '0.00'}</p>
                    <p><strong>Transações encontradas:</strong> {testResult.transacoes_recentes || 0}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Resultado da sincronização */}
        {resultado && (
          <div className={`p-4 rounded-lg ${resultado.erro ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}`}>
            {resultado.erro ? (
              <div className="flex items-start">
                <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0" />
                <div>
                  <p className="font-medium text-red-900">Erro na sincronização</p>
                  <p className="text-sm text-red-700 mt-1">{resultado.erro}</p>
                </div>
              </div>
            ) : (
              <div>
                <div className="flex items-center text-green-700 mb-4">
                  <CheckCircle className="h-5 w-5 mr-2" />
                  <span className="font-medium">
                    {resultado.sucesso.length} transação(ões) importada(s)!
                  </span>
                </div>
                
                {resultado.sucesso.length > 0 && (
                  <div className="max-h-48 overflow-y-auto space-y-2">
                    {resultado.sucesso.slice(0, 5).map((t, i) => (
                      <div key={i} className="bg-white p-2 rounded text-sm">
                        <div className="flex justify-between">
                          <span className="font-medium text-gray-900">{t.descricao}</span>
                          <span className={t.tipo === 'entrada' ? 'text-green-600' : 'text-red-600'}>
                            {t.tipo === 'entrada' ? '+' : '-'} R$ {t.valor.toFixed(2)}
                          </span>
                        </div>
                        <div className="text-gray-500 text-xs">
                          {new Date(t.data).toLocaleDateString('pt-BR')}
                        </div>
                      </div>
                    ))}
                    {resultado.sucesso.length > 5 && (
                      <p className="text-sm text-green-700 text-center">
                        + {resultado.sucesso.length - 5} transações adicionais
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Instruções */}
      {instrucoes && (
        <div className="card mt-6">
          <h3 className="font-medium text-gray-900 mb-4 flex items-center">
            <HelpCircle className="h-5 w-5 mr-2 text-primary-600" />
            Como obter seu Access Token
          </h3>
          
          <ol className="space-y-4">
            {instrucoes.steps.map((step: any) => (
              <li key={step.step} className="flex">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-sm font-medium mr-3">
                  {step.step}
                </span>
                <div>
                  <p className="font-medium text-gray-900">{step.title}</p>
                  <p className="text-sm text-gray-600 mt-0.5">{step.description}</p>
                </div>
              </li>
            ))}
          </ol>

          <div className="mt-6 pt-4 border-t border-gray-200">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Notas importantes:</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              {instrucoes.important_notes.map((note: string, i: number) => (
                <li key={i} className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  {note}
                </li>
              ))}
            </ul>
          </div>

          <a
            href="https://www.mercadopago.com.br/developers"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-6 inline-flex items-center text-primary-600 hover:text-primary-700 text-sm font-medium"
          >
            Acessar Mercado Pago Developers
            <ExternalLink className="h-4 w-4 ml-1" />
          </a>
        </div>
      )}
    </div>
  )
}
