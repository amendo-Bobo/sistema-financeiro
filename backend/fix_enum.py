"""Script para corrigir o enum do banco"""
from sqlalchemy import create_engine, text
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)

def fix_enum():
    """Corrige o enum tipo_transacao para usar valores corretos"""
    
    with engine.connect() as conn:
        # Verificar valores atuais
        result = conn.execute(text("SELECT unnest(enum_range(NULL::tipo_transacao_enum))"))
        current_values = [row[0] for row in result]
        print(f"Valores atuais no enum: {current_values}")
        
        # Drop do enum antigo
        conn.execute(text("DROP TYPE IF EXISTS tipo_transacao_enum CASCADE"))
        
        # Criar novo enum com valores corretos
        conn.execute(text("""
            CREATE TYPE tipo_transacao_enum AS ENUM ('entrada', 'saida')
        """))
        
        # Commit
        conn.commit()
        print("Enum corrigido com sucesso!")

if __name__ == "__main__":
    fix_enum()
