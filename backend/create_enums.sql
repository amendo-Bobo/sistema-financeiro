-- Criar os enums manualmente no Supabase
-- Execute este SQL diretamente no Supabase SQL Editor

-- 1. Criar tipo_transacao_enum
CREATE TYPE tipo_transacao_enum AS ENUM ('ENTRADA', 'SAIDA');

-- 2. Criar categoria_transacao_enum  
CREATE TYPE categoria_transacao_enum AS ENUM (
    'ALIMENTACAO', 
    'TRANSPORTE', 
    'MORADIA', 
    'SAUDE', 
    'EDUCACAO', 
    'LAZER', 
    'VESTUARIO', 
    'UTILIDADES', 
    'SALARIO', 
    'INVESTIMENTOS', 
    'OUTROS'
);

-- 3. Converter coluna tipo da tabela transacoes
ALTER TABLE transacoes 
ALTER COLUMN tipo TYPE tipo_transacao_enum 
USING 
    CASE 
        WHEN tipo = 'ENTRADA' THEN 'ENTRADA'::tipo_transacao_enum
        WHEN tipo = 'SAIDA' THEN 'SAIDA'::tipo_transacao_enum
        ELSE 'SAIDA'::tipo_transacao_enum
    END;

-- 4. Converter coluna categoria da tabela transacoes
ALTER TABLE transacoes 
ALTER COLUMN categoria TYPE categoria_transacao_enum 
USING 
    CASE 
        WHEN categoria = 'ALIMENTACAO' THEN 'ALIMENTACAO'::categoria_transacao_enum
        WHEN categoria = 'TRANSPORTE' THEN 'TRANSPORTE'::categoria_transacao_enum
        WHEN categoria = 'MORADIA' THEN 'MORADIA'::categoria_transacao_enum
        WHEN categoria = 'SAUDE' THEN 'SAUDE'::categoria_transacao_enum
        WHEN categoria = 'EDUCACAO' THEN 'EDUCACAO'::categoria_transacao_enum
        WHEN categoria = 'LAZER' THEN 'LAZER'::categoria_transacao_enum
        WHEN categoria = 'VESTUARIO' THEN 'VESTUARIO'::categoria_transacao_enum
        WHEN categoria = 'UTILIDADES' THEN 'UTILIDADES'::categoria_transacao_enum
        WHEN categoria = 'SALARIO' THEN 'SALARIO'::categoria_transacao_enum
        WHEN categoria = 'INVESTIMENTOS' THEN 'INVESTIMENTOS'::categoria_transacao_enum
        WHEN categoria = 'OUTROS' THEN 'OUTROS'::categoria_transacao_enum
        ELSE 'OUTROS'::categoria_transacao_enum
    END;

-- 5. Converter coluna categoria da tabela orcamentos_mensais
ALTER TABLE orcamentos_mensais 
ALTER COLUMN categoria TYPE categoria_transacao_enum 
USING 
    CASE 
        WHEN categoria = 'ALIMENTACAO' THEN 'ALIMENTACAO'::categoria_transacao_enum
        WHEN categoria = 'TRANSPORTE' THEN 'TRANSPORTE'::categoria_transacao_enum
        WHEN categoria = 'MORADIA' THEN 'MORADIA'::categoria_transacao_enum
        WHEN categoria = 'SAUDE' THEN 'SAUDE'::categoria_transacao_enum
        WHEN categoria = 'EDUCACAO' THEN 'EDUCACAO'::categoria_transacao_enum
        WHEN categoria = 'LAZER' THEN 'LAZER'::categoria_transacao_enum
        WHEN categoria = 'VESTUARIO' THEN 'VESTUARIO'::categoria_transacao_enum
        WHEN categoria = 'UTILIDADES' THEN 'UTILIDADES'::categoria_transacao_enum
        WHEN categoria = 'SALARIO' THEN 'SALARIO'::categoria_transacao_enum
        WHEN categoria = 'INVESTIMENTOS' THEN 'INVESTIMENTOS'::categoria_transacao_enum
        WHEN categoria = 'OUTROS' THEN 'OUTROS'::categoria_transacao_enum
        ELSE 'OUTROS'::categoria_transacao_enum
    END;
