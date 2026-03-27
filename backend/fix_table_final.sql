-- Mudar colunas para string para resolver problema de enum
ALTER TABLE transacoes ALTER COLUMN tipo TYPE VARCHAR(20);
ALTER TABLE transacoes ALTER COLUMN categoria TYPE VARCHAR(50);

-- Adicionar check constraints para validação
ALTER TABLE transacoes ADD CONSTRAINT check_tipo_transacao CHECK (tipo IN ('entrada', 'saida'));
ALTER TABLE transacoes ADD CONSTRAINT check_categoria_transacao CHECK (categoria IN ('alimentacao', 'transporte', 'moradia', 'saude', 'educacao', 'lazer', 'vestuario', 'utilidades', 'salario', 'investimentos', 'outros'));
