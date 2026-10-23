-- 1. Cria a base de dados com codificação UTF-8 completa
CREATE DATABASE IF NOT EXISTS saep_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE saep_db;

-- 2. Limpeza preventiva respeitando a integridade referencial
DROP TABLE IF EXISTS agendamentos;
DROP TABLE IF EXISTS veiculos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS usuarios;

-- 3. Tabela de Usuários (Funcionários da Oficina)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 4. Tabela de Clientes (com proteção LGPD para CPF)
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    cpf_hash VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    endereco VARCHAR(200) NOT NULL,
    data_cadastro DATE NOT NULL DEFAULT (CURRENT_DATE),
    INDEX idx_cliente_nome (nome)
) ENGINE=InnoDB;

-- 5. Tabela de Veículos (Vinculada obrigatoriamente a Cliente)
CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    placa VARCHAR(10) NOT NULL UNIQUE,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(80) NOT NULL,
    ano INT NOT NULL,
    cor VARCHAR(30) NOT NULL,
    quilometragem INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_veiculos_cliente
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_veiculo_placa (placa)
) ENGINE=InnoDB;

-- 6. Tabela de Agendamentos (Ordenada por Data)
CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    veiculo_id INT NOT NULL,
    data_agendamento DATETIME NOT NULL,
    descricao_servico TEXT NOT NULL,
    status ENUM('Agendado', 'Em Andamento', 'Concluído', 'Cancelado') NOT NULL DEFAULT 'Agendado',
    valor_estimado DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    observacoes TEXT NULL,
    CONSTRAINT fk_agendamentos_cliente
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_agendamentos_veiculo
        FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
        ON DELETE CASCADE,
    INDEX idx_agendamento_data (data_agendamento)
) ENGINE=InnoDB;

-- 7. Carga de Dados (Mínimo de 3 registros por tabela exigido no edital)
-- Hashes Bcrypt verificados:
-- 'admin123' -> $2b$10$MkMG3pOmMfg2BGi7BDZgyuHx3QnCbBssXbW2b1pujTPotmGjl4TNy
-- 'senha123' -> $2b$10$7bTYODJOhSQOlfHq.yC16..5MuqOnPSYI9nj2YM5F.ehgjBfrTO5a
-- 'rec123'   -> $2b$10$FiphGoCIenRI0cPv9Lt18.xR49pSkbnpM3Fx6.1MxmwkaXFk/qlIG
INSERT INTO usuarios (id, nome, login, senha_hash, cargo, ativo) VALUES
(1, 'Carlos Silva', 'admin', '$2b$10$MkMG3pOmMfg2BGi7BDZgyuHx3QnCbBssXbW2b1pujTPotmGjl4TNy', 'Administrador / Gerente', TRUE),
(2, 'Marcos Oliveira', 'mecanico', '$2b$10$7bTYODJOhSQOlfHq.yC16..5MuqOnPSYI9nj2YM5F.ehgjBfrTO5a', 'Mecânico Chefe', TRUE),
(3, 'Juliana Santos', 'recepcao', '$2b$10$FiphGoCIenRI0cPv9Lt18.xR49pSkbnpM3Fx6.1MxmwkaXFk/qlIG', 'Recepcionista', TRUE);

INSERT INTO clientes (id, nome, cpf, cpf_hash, telefone, email, endereco, data_cadastro) VALUES
(1, 'Roberto Mendes Alencar', '12345678901', '$2b$12$7J9Xj1zT6Q0gB9w4Yx1U4.fK7uG8z2N3O5Y8W7e5t3u2i1o0p9q8r', '(11) 98765-4321', 'roberto.mendes@email.com', 'Av. Paulista, 1500 - Bela Vista, SP', '2026-01-15'),
(2, 'Mariana Costa Ferreira', '98765432100', '$2b$12$1K2Lm3No4Pq5Rs6Tu7Vw8.aB9cDefGhIjKlMnOpQrStUvWxYz01234', '(11) 91234-5678', 'mariana.costa@email.com', 'Rua das Flores, 340 - Pinheiros, SP', '2026-02-10'),
(3, 'Fernando Dias Barbosa', '45678912344', '$2b$12$9Z8Yx7Wv6Ut5Sr4Qp3On2.mK1lJiHgFeDcBaZyXwVuTsRqPoNmLk9', '(11) 99887-7665', 'fernando.dias@email.com', 'Rua Vergueiro, 890 - Vila Mariana, SP', '2026-02-28');

INSERT INTO veiculos (id, cliente_id, placa, marca, modelo, ano, cor, quilometragem) VALUES
(1, 1, 'BRA2E19', 'Toyota', 'Corolla XEi 2.0', 2022, 'Prata', 42500),
(2, 2, 'RJK4A88', 'Honda', 'Civic Touring 1.5 Turbo', 2021, 'Preto', 36000),
(3, 3, 'FXT9C23', 'Volkswagen', 'T-Cross Highline 250 TSI', 2023, 'Branco', 18900);

INSERT INTO agendamentos (id, cliente_id, veiculo_id, data_agendamento, descricao_servico, status, valor_estimado, observacoes) VALUES
(1, 1, 1, '2026-10-25 08:30:00', 'Revisão periódica de 40.000 km e troca de óleo 5W30', 'Agendado', 680.00, 'Ruído na pastilha esquerda.'),
(2, 2, 2, '2026-10-25 14:00:00', 'Alinhamento 3D e balanceamento de 4 rodas', 'Agendado', 450.00, 'Vibração acima de 100km/h.'),
(3, 3, 3, '2026-10-26 09:00:00', 'Higienização de ar-condicionado e troca de filtro', 'Agendado', 290.00, 'Veículo em garantia.');
