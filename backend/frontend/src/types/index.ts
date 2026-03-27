export interface User {
  id: number
  email: string
  nome: string
  is_active: boolean
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  nome: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export type TipoTransacao = 'ENTRADA' | 'SAIDA'

export type CategoriaTransacao = 
  | 'ALIMENTACAO' 
  | 'TRANSPORTE' 
  | 'MORADIA' 
  | 'SAUDE' 
  | 'EDUCACAO' 
  | 'LAZER' 
  | 'VESTUARIO' 
  | 'UTILIDADES' 
  | 'SALARIO' 
  | 'INVESTIMENTOS' 
  | 'OUTROS'

export interface Transacao {
  id: number
  usuario_id: number
  descricao: string
  valor: number
  tipo: TipoTransacao
  categoria: CategoriaTransacao
  data: string
  is_fixa: boolean
  is_recorrente: boolean
  observacoes: string | null
  categoria_personalizada_id: number | null
  created_at: string
  updated_at: string
}

export interface TransacaoCreate {
  descricao: string
  valor: number
  tipo: TipoTransacao
  categoria: CategoriaTransacao
  data: string
  is_fixa?: boolean
  is_recorrente?: boolean
  observacoes?: string
  categoria_personalizada_id?: number
}

export interface TransacaoResumo {
  total_entradas: number
  total_saidas: number
  saldo: number
  quantidade_transacoes: number
}

export interface ContaBancaria {
  id: number
  usuario_id: number
  nome_banco: string
  agencia: string | null
  conta: string | null
  tipo_conta: string | null
  saldo: number
  is_active: boolean
  integracao_tipo: string | null
  ultima_sincronizacao: string | null
  created_at: string
  updated_at: string
}

export interface DashboardResumo {
  saldo_atual: number
  total_entradas_mes: number
  total_saidas_mes: number
  balanco_mes: number
  transacoes_recentes: Transacao[]
  alertas_orcamento: OrcamentoResumo[]
}

export interface OrcamentoResumo {
  categoria: CategoriaTransacao
  orcado: number
  gasto_real: number
  diferenca: number
  percentual_usado: number
}

export interface GraficoDados {
  labels: string[]
  valores: number[]
  cores?: string[]
}
