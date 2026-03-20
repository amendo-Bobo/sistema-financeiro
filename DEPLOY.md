# Sistema Financeiro

## Deploy em Produção - Render

### 🚀 Passos para deploy:

1. **Fazer upload no GitHub**
   ```bash
   git init
   git add .
   git commit -m "Ready for production"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/sistema-financeiro.git
   git push -u origin main
   ```

2. **Configurar banco de dados**
   - Criar conta no [Supabase](https://supabase.com) (grátis)
   - Criar novo projeto
   - Copiar string de conexão

3. **Fazer deploy no Render**
   - Criar conta no [Render](https://render.com)
   - Conectar GitHub
   - Criar "Web Service"
   - Configurar variáveis de ambiente

### 🔧 Variáveis de Ambiente (Render):

```
DATABASE_URL=postgresql://postgres:[SUA-SENHA]@db.[SEU-PROJETO].supabase.co:5432/postgres
SECRET_KEY=[SUA-SECRET-KEY-AQUI]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 🌐 URLs finais:
- Backend: `https://sistema-financeiro.onrender.com`
- Frontend: `https://sistema-financeiro.onrender.com` (mesmo URL)
- Acesso de qualquer lugar!
