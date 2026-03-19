import axios from 'axios'
import type { LoginCredentials, RegisterData, AuthResponse, User, Transacao } from '../types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const params = new URLSearchParams()
    params.append('username', credentials.email)
    params.append('password', credentials.password)
    
    const response = await api.post<AuthResponse>('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  },
}

export const transacaoService = {
  async getTransacoes(params?: any): Promise<Transacao[]> {
    // Adicionar timestamp para evitar cache
    const cacheBuster = Date.now()
    const url = params ? `/transacoes/?${new URLSearchParams({...params, _t: cacheBuster.toString()})}` : `/transacoes/?_t=${cacheBuster}`
    const response = await api.get(url)
    return response.data
  },

  async getTransacao(id: number) {
    const response = await api.get(`/transacoes/${id}`)
    return response.data
  },

  async createTransacao(data: any) {
    const response = await api.post('/transacoes/', data)
    return response.data
  },

  async updateTransacao(id: number, data: any) {
    const response = await api.put(`/transacoes/${id}`, data)
    return response.data
  },

  async deleteTransacao(id: number) {
    const response = await api.delete(`/transacoes/${id}`)
    return response.data
  },

  async getResumoMensal(ano?: number, mes?: number) {
    const response = await api.get('/transacoes/resumo/mensal', {
      params: { ano, mes }
    })
    return response.data
  },

  async getGastosPorCategoria(ano?: number, mes?: number) {
    const response = await api.get('/transacoes/graficos/gastos-por-categoria', {
      params: { ano, mes }
    })
    return response.data
  },
}

export const dashboardService = {
  async getResumo() {
    const response = await api.get('/dashboard/resumo')
    return response.data
  },

  async getEvolucaoMensal(meses?: number) {
    const response = await api.get('/dashboard/evolucao-mensal', {
      params: { meses }
    })
    return response.data
  },
}

export const contaService = {
  async getContas() {
    const response = await api.get('/contas/')
    return response.data
  },

  async createConta(data: any) {
    const response = await api.post('/contas/', data)
    return response.data
  },

  async updateConta(id: number, data: any) {
    const response = await api.put(`/contas/${id}`, data)
    return response.data
  },

  async deleteConta(id: number) {
    const response = await api.delete(`/contas/${id}`)
    return response.data
  },
}

export const importacaoService = {
  async importarArquivo(file: File, banco: string = 'auto') {
    const formData = new FormData()
    formData.append('arquivo', file)
    formData.append('banco', banco)
    
    const response = await api.post('/importar/arquivo', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async getBancosSuportados() {
    const response = await api.get('/importar/bancos-suportados')
    return response.data
  },
}

export const mercadoPagoService = {
  async configurar(accessToken: string) {
    const response = await api.post('/mercadopago/configurar', {
      access_token: accessToken,
    })
    return response.data
  },

  async sincronizar(accessToken: string, days: number = 30) {
    const response = await api.post('/mercadopago/sync-with-token', null, {
      params: {
        access_token: accessToken,
        days,
      },
    })
    return response.data
  },

  async getInstrucoes() {
    const response = await api.get('/mercadopago/instrucoes')
    return response.data
  },

  async testarToken(token: string) {
    const response = await api.get(`/mercadopago/testar-token/${token}`)
    return response.data
  },
}

export default api
