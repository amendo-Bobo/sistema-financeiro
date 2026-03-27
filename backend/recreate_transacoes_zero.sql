-- RECRIAR TABELA TRANSACOES DO ZERO COM ENUMS CORRETOS

-- 1. Drop da tabela antiga
DROP TABLE IF EXISTS transacoes CASCADE;

-- 2. Recriar com os enums corretos
CREATE TABLE transacoes (
  id integer NOT NULL DEFAULT nextval('transacoes_id_seq'::regclass),
  usuario_id integer NOT NULL,
  descricao character varying NOT NULL,
  valor numeric NOT NULL,
  tipo tipo_transacao_enum NOT NULL DEFAULT 'SAIDA',
  categoria categoria_transacao_enum DEFAULT 'OUTROS',
  categoria_personalizada_id integer,
  data date,
  is_fixa boolean DEFAULT false,
  is_recorrente boolean DEFAULT false,
  observacoes text,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT transacoes_pkey PRIMARY KEY (id),
  CONSTRAINT transacoes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.users(id),
  CONSTRAINT transacoes_categoria_personalizada_id_fkey FOREIGN KEY (categoria_personalizada_id) REFERENCES public.categorias_personalizadas(id)
);

-- 3. Recriar a sequência
DROP SEQUENCE IF EXISTS transacoes_id_seq;
CREATE SEQUENCE transacoes_id_seq START 1 INCREMENT 1 NO MINVALUE NO MAXVALUE CACHE 1;

-- 4. Resetar o valor da sequência
ALTER SEQUENCE transacoes_id_seq OWNED BY transacoes.id;
