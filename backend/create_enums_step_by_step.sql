-- PASSO 1: Criar tipo_transacao_enum
CREATE TYPE tipo_transacao_enum AS ENUM ('ENTRADA', 'SAIDA');

-- PASSO 2: Criar categoria_transacao_enum  
CREATE TYPE categoria_transacao_enum AS ENUM ('ALIMENTACAO', 'TRANSPORTE', 'MORADIA', 'SAUDE', 'EDUCACAO', 'LAZER', 'VESTUARIO', 'UTILIDADES', 'SALARIO', 'INVESTIMENTOS', 'OUTROS');

-- PASSO 3: Converter coluna tipo (se der erro, ignore por enquanto)
-- ALTER TABLE transacoes ALTER COLUMN tipo TYPE tipo_transacao_enum USING 'ENTRADA'::tipo_transacao_enum;

-- PASSO 4: Converter coluna categoria (se der erro, ignore por enquanto)
-- ALTER TABLE transacoes ALTER COLUMN categoria TYPE categoria_transacao_enum USING 'OUTROS'::categoria_transacao_enum;

-- PASSO 5: Converter orcamentos_mensais (se der erro, ignore por enquanto)
-- ALTER TABLE orcamentos_mensais ALTER COLUMN categoria TYPE categoria_transacao_enum USING 'OUTROS'::categoria_transacao_enum;
