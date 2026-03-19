# Sistema de Finanças Pessoais

Sistema completo para controle de finanças pessoais com backend em FastAPI (Python) e frontend em React com TypeScript.

## Funcionalidades

- **Gestão de Transações**: Cadastro de entradas e saídas com categorias
- **Dashboard**: Visualização de saldo, entradas/saídas do mês e gráficos
- **Contas Bancárias**: Cadastro e acompanhamento de múltiplas contas
- **Autenticação**: Sistema de login e registro de usuários
- **Filtros**: Busca de transações por tipo, categoria e período
- **Orçamentos**: Definição de limites por categoria (alertas quando próximo do limite)

## Estrutura do Projeto

```
sistema-financas/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── auth/        # Autenticação
│   │   ├── crud/        # Operações CRUD
│   │   ├── models/      # Modelos SQLAlchemy
│   │   ├── routers/     # Endpoints da API
│   │   ├── schemas/     # Schemas Pydantic
│   │   ├── services/    # Serviços
│   │   ├── utils/       # Utilitários
│   │   ├── config.py    # Configurações
│   │   ├── database.py  # Configuração DB
│   │   └── main.py      # App principal
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/             # React + TypeScript
    ├── src/
    │   ├── components/  # Componentes reutilizáveis
    │   ├── contexts/    # Contextos React
    │   ├── hooks/       # Hooks customizados
    │   ├── pages/       # Páginas da aplicação
    │   ├── services/    # Serviços de API
    │   ├── types/       # Tipos TypeScript
    │   └── utils/       # Utilitários
    ├── package.json
    └── vite.config.ts
```

## Instalação e Execução

### Backend

1. Acesse a pasta do backend:
```bash
cd backend
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute o servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

O backend estará disponível em `http://localhost:8000`

Documentação da API: `http://localhost:8000/docs`

### Frontend

1. Acesse a pasta do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **JWT**: Autenticação via tokens
- **SQLite**: Banco de dados (pode ser trocado por PostgreSQL)

### Frontend
- **React 18**: Biblioteca UI
- **TypeScript**: Tipagem estática
- **Vite**: Build tool rápida
- **Tailwind CSS**: Framework CSS utilitário
- **Recharts**: Gráficos e visualizações
- **React Router**: Navegação
- **Axios**: Cliente HTTP
- **Lucide React**: Ícones

## Integração Bancária

O sistema foi preparado para integração com bancos via **Plaid** ou **Open Banking Brasileiro**. Para ativar:

1. Obtenha credenciais no [Plaid](https://plaid.com) ou no [Open Banking Brasil](https://openbankingbrasil.org.br)
2. Configure as variáveis no arquivo `.env`
3. Implemente o fluxo de autenticação OAuth2 no módulo `app/services/`

## Scripts Úteis

### Backend
```bash
# Criar migrations
alembic revision --autogenerate -m "descrição"

# Aplicar migrations
alembic upgrade head

# Executar testes
pytest
```

### Frontend
```bash
# Build para produção
npm run build

# Preview da build
npm run preview
```

## Segurança

- Senhas são hasheadas com bcrypt
- Autenticação via JWT com expiração
- CORS configurado para origens específicas
- SQL injection protegido via SQLAlchemy ORM

## Próximos Passos / Melhorias Futuras

- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Importação de extratos bancários (OFX, CSV)
- [ ] Notificações de alertas por email
- [ ] App mobile (React Native)
- [ ] Multi-currency suporte
- [ ] Metas financeiras
- [ ] Previsões baseadas em histórico

## Licença

MIT License - Sinta-se livre para usar e modificar!

## Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
