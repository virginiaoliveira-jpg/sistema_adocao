CREATE TABLE usuario (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	senha VARCHAR(200) NOT NULL, 
	tipo VARCHAR(20) NOT NULL, 
	cpf VARCHAR(20), 
	telefone VARCHAR(20), 
	endereco VARCHAR(200), 
	data_nascimento VARCHAR(20), 
	tipo_residencia VARCHAR(50), 
	outros_animais VARCHAR(10), 
	motivo_adocao TEXT, 
	cnpj VARCHAR(20), 
	razao_social VARCHAR(100), 
	responsavel_nome VARCHAR(100), 
	responsavel_cpf VARCHAR(20), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE animal (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	especie VARCHAR(50) NOT NULL, 
	raca VARCHAR(50), 
	idade VARCHAR(20), 
	status VARCHAR(20), 
	localizacao VARCHAR(100), 
	foto VARCHAR(200), 
	vacinacao TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE adotante (
	id INTEGER NOT NULL, 
	usuario_id INTEGER, 
	nome VARCHAR(100) NOT NULL, 
	cpf VARCHAR(20) NOT NULL, 
	telefone VARCHAR(20) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	endereco VARCHAR(200) NOT NULL, 
	data_nascimento VARCHAR(20), 
	tipo_residencia VARCHAR(50), 
	outros_animais VARCHAR(10), 
	motivo_adocao TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuario (id)
);

CREATE TABLE adocao (
	id INTEGER NOT NULL, 
	animal_id INTEGER NOT NULL, 
	adotante_id INTEGER NOT NULL, 
	data_adocao DATETIME, 
	motivo TEXT, 
	status VARCHAR(50), 
	PRIMARY KEY (id), 
	FOREIGN KEY(animal_id) REFERENCES animal (id), 
	FOREIGN KEY(adotante_id) REFERENCES adotante (id)
);

