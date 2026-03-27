-- Criar os enums manualmente no Supabase
-- Execute este SQL diretamente no Supabase SQL Editor

-- 1. Criar tipo_transacao_enum
CREATE TYPE tipo_transacao_enum AS ENUM ('ENTRADA', 'SAIDA');

-- 2. Criar categoria_transacao_enum
CREATE TYPE categoria_transacao_enum AS ENUM ('ALIMENTACAO', 'TRANSPORTE', 'MORADIA', 'SAUDE', 'EDUCACAO', 'LAZER', 'VESTUARIO', 'UTILIDADES', 'SALARIO', 'INVESTIMENTOS', 'OUTROS');

-- 3. Converter coluna tipo da tabela transacoes
ALTER TABLE transacoes ALTER COLUMN tipo TYPE tipo_transacao_enum USING 'ENTRADA'::tipo_transacao_enum;

-- 4. Converter coluna categoria da tabela transacoes
ALTER TABLE transacoes ALTER COLUMN categoria TYPE categoria_transacao_enum USING 'OUTROS'::categoria_transacao_enum;

-- 5. Converter coluna categoria da tabela orcamentos_mensais
ALTER TABLE orcamentos_mensais ALTER COLUMN categoria TYPE categoria_transacao_enum USING 'OUTROS'::categoria_transacao_enum;
