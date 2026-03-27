"""Script para corrigir os enums do banco"""
from sqlalchemy import create_engine, text
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)

def fix_database():
    """Corrige os enums do banco"""
    
    with engine.connect() as conn:
        # 1. Remover constraints temporariamente
        conn.execute(text("ALTER TABLE transacoes DROP CONSTRAINT IF EXISTS transacoes_tipo_check"))
        conn.execute(text("ALTER TABLE transacoes DROP CONSTRAINT IF EXISTS transacoes_categoria_check"))
        
        # 2. Drop dos enums antigos
        conn.execute(text("DROP TYPE IF EXISTS tipo_transacao_enum CASCADE"))
        conn.execute(text("DROP TYPE IF EXISTS categoria_transacao_enum CASCADE"))
        
        # 3. Criar enums com valores corretos
        conn.execute(text("""
            CREATE TYPE tipo_transacao_enum AS ENUM ('entrada', 'saida')
        """))
        
        conn.execute(text("""
            CREATE TYPE categoria_transacao_enum AS ENUM (
                'alimentacao', 'transporte', 'moradia', 'saude', 
                'educacao', 'lazer', 'vestuario', 'utilidades', 
                'salario', 'investimentos', 'outros'
            )
        """))
        
        # 4. Alterar colunas para usar os novos enums
        conn.execute(text("""
            ALTER TABLE transacoes 
            ALTER COLUMN tipo TYPE tipo_transacao_enum 
            USING tipo::text::tipo_transacao_enum
        """))
        
        conn.execute(text("""
            ALTER TABLE transacoes 
            ALTER COLUMN categoria TYPE categoria_transacao_enum 
            USING categoria::text::categoria_transacao_enum
        """))
        
        # 5. Corrigir orcamentos_mensais
        conn.execute(text("""
            ALTER TABLE orcamentos_mensais 
            ALTER COLUMN categoria TYPE categoria_transacao_enum 
            USING categoria::text::categoria_transacao_enum
        """))
        
        conn.commit()
        print("Banco corrigido com sucesso!")

if __name__ == "__main__":
    fix_database()
