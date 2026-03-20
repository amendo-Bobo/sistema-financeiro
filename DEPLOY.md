# Sistema Financeiro

## Deploy em Produção - Render

### 🚀 Passos para deploy:

1. **Fazer upload no GitHub**
   ```bash
   git init
   git add .
   git commit -m "Ready for production"
   git branch -M main
   git remote add origin https://github.com/emendo-Bobo/financia.git
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
DATABASE_URL=postgresql://postgres:[Hr162005]@db.gbnibcoshpgwzqkkugsb.supabase.co:5432/postgres
SECRET_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdibmliY29zaHBnd3pxa2t1Z3NiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5NDYxNDYsImV4cCI6MjA4OTUyMjE0Nn0.SoAvxOGG4Q6eNGgNco5b7KAYaQ9cwgkgdcGGX6CHx5Q
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 🌐 URLs finais:
- Backend: `https://sistema-financeiro.onrender.com`
- Frontend: `https://sistema-financeiro.onrender.com` (mesmo URL)
- Acesso de qualquer lugar!
