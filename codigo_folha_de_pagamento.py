# Código de Lucas Pereira e Victor Santana

import os
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Criando banco de dados.
MEU_BANCO = create_engine("sqlite:///folhapagamento.db")

# Criando conexão com banco de dados.
Session = sessionmaker(bind=MEU_BANCO)
session = Session()

# Criando tabela.
Base = declarative_base()

class Funcionario(Base):
    __tablename__ = "funcionarios"

    # Definindo campos da tabela.
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    matricula = Column("matricula", String)
    senha = Column("senha", String)
    nome = Column("nome", String)
    salario_base = Column("salario_base", Float)

    # Definindo atributos da classe.
    def __init__(self, matricula: str, senha: str, nome: str, salario_base: float):
        self.matricula = matricula
        self.senha = senha
        self.nome = nome
        self.salario_base = salario_base

# Criando tabela no banco de dados.
Base.metadata.create_all(bind=MEU_BANCO)

def calcular_inss(salario):
    if salario <= 1100.00:
        return salario * 0.075
    elif salario <= 2203.48:
        return salario * 0.09
    elif salario <= 3305.22:
        return salario * 0.12
    elif salario <= 6433.57:
        return salario * 0.14
    else:
        return 854.36

def calcular_irrf(salario, dependentes):
    faixa_irrf = [
        (2259.20, 0.0),
        (2826.65, 0.075),
        (3751.05, 0.15),
        (4664.68, 0.225),
        (float('inf'), 0.275)
    ]
    deducao_dependente = 189.59
    for limite, taxa in faixa_irrf:
        if salario <= limite:
            return (salario * taxa) - (deducao_dependente * dependentes)

def calcular_salario_liquido(funcionario):
    inss = calcular_inss(funcionario.salario_base)
    irrf = calcular_irrf(funcionario.salario_base, 1)  # considerando 1 dependente
    return funcionario.salario_base - inss - irrf

# Salvar no banco de dados.
os.system("cls || clear")

# Inserindo um funcionário
print("Solicitando dados do funcionário.")
matricula = input("Digite sua matrícula: ")
senha = input("Digite sua senha: ")
nome = input("Digite seu nome: ")
salario_base = float(input("Digite seu salário base: R$ "))

funcionario = Funcionario(matricula=matricula, senha=senha, nome=nome, salario_base=salario_base)
session.add(funcionario)
session.commit()

# Acesso aos dados do funcionário
print("\nAcessando dados do funcionário.")
matricula_acesso = input("Digite sua matrícula: ")
senha_acesso = input("Digite sua senha: ")

funcionario_acesso = session.query(Funcionario).filter_by(matricula=matricula_acesso, senha=senha_acesso).first()

if funcionario_acesso:
    vale_transporte = input("Deseja receber vale transporte (s/n)? ").strip().lower()
    vale_refeicao = float(input("Digite o valor do vale refeição fornecido pela empresa: R$ "))

    salario_liquido = calcular_salario_liquido(funcionario_acesso)

    if vale_transporte == 's':
        desconto_transporte = funcionario_acesso.salario_base * 0.06
        salario_liquido -= desconto_transporte

    desconto_refeicao = vale_refeicao * 0.20
    salario_liquido -= desconto_refeicao

    print(f"\nSalário líquido de {funcionario_acesso.nome}: R$ {salario_liquido:.2f}")
else:
    print("Matrícula ou senha incorretas.")

# Fechando conexão.
session.close()
