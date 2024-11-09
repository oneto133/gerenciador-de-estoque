from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import OperationalError, IntegrityError
from Funções import Horarios
import pandas as pd

from sqlalchemy import select, text
import csv
import asyncio
class Conexao:
    def __init__(self, nome_completo='', nome='', senha='', email=''):
        self.banco = create_engine('postgresql://postgres:M7cIWJYjxBodNojL@uncertainly-pretty-chimaera.data-1.use1.tembo.io:5432/postgres')
    
    def inserir_dados(self, nome_completo, nome, senha, email):
        try:
            with self.banco.connect() as conn:
                with conn.begin():
                    self.inserir_dados = text(f"INSERT INTO usuarios (nome_completo, nome_usuario, senha, email) VALUES ('{nome_completo}','{nome}', '{senha}', '{email}')")
                    conn.execute(self.inserir_dados)
                    return "executado com sucesso!"
        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")
        except IntegrityError as e:
                return(f"Violação de integridade: {e}")
        except Exception as e:
            return(f"Erro inesperado: {e}")
    
class Query():
    def __init__(self, consulta=''):
        self.async_engine = create_async_engine('postgresql+asyncpg://postgres:M7cIWJYjxBodNojL@uncertainly-pretty-chimaera.data-1.use1.tembo.io:5432/postgres')
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)

    async def consultar_senha_por_usuario(self, consulta):
        try:
            async with self.async_session() as conn:
                inserir_dados = text(f"select senha from usuarios where nome_usuario = '{consulta}'")
                result = await conn.execute(inserir_dados)
                for row in result:
                    return self.tratar_resultado_de_consulta(row)
        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")
        except IntegrityError as e:
            return(f"Violação de integridade: {e}")
        except ConnectionResetError as e:
            return (f"Erro de conexão: {e}")
        except Exception as e:
            return(f"Erro inesperado: {e}")

    def tratar_resultado_de_consulta(self, dado):
        self.dado = str(dado)
        return self.dado[2:-3]


class Cadastrar_produtos:
    
    def __init__(self, conexão="//postgres:M7cIWJYjxBodNojL@uncertainly-pretty-chimaera.data-1.use1.tembo.io:5432/postgres"):

    #Adicionando os parâmetros a variáveis

        self.hora = Horarios()
        self.data = self.hora.data_atual()
        self.async_engine = create_async_engine(f'postgresql+asyncpg:{conexão}')
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)


    async def inserir_dados(self, codigo_interno=None, ean="", descrição="", preco=10.00, quantidade=1, unidade_medida="", categoria="", 
    ultima_venda="1999-12-24", fornecedor="", observações=""):

        self.codigo_interno = codigo_interno
        self.ean = ean
        self.descrição = descrição
        self.preco = preco
        self.quantidade = quantidade
        self.unidade_medida = unidade_medida
        self.categoria = categoria
        self.ultima_venda = ultima_venda
        self.fornecedor = fornecedor
        self.observações = observações



        try:
            async with self.async_session() as conn:
                inserir_dados = text("INSERT INTO estoque (codigo_interno, ean, descricao, preco,"
                "quantidade, unidade_medida, categoria, data_adicao, ultima_venda, fornecedor,"
                f"observacoes) VALUES ('{self.codigo_interno}', '{self.ean}', '{self.descrição}', {self.preco}, {self.quantidade},"
                f"'{self.unidade_medida}', '{self.categoria}', '{self.data}', '{self.ultima_venda}', '{self.fornecedor}',"
                f"'{self.observações}')")
                result = await conn.execute(inserir_dados)
                await conn.commit()
                return f"Dados inseridos com sucesso!"
        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")

        except IntegrityError as e:
            return "Verifique os dados e tente novamente, lembre-se de inserir o código interno do produto"
        except Exception as e:
            return e

class consulta:
    hora = Horarios()
    data = hora.data_atual()
    def __init__(self, conexão="//postgres:M7cIWJYjxBodNojL@uncertainly-pretty-chimaera.data-1.use1.tembo.io:5432/postgres",
        codigo_interno=None, ean="", descrição="", preco=10.00, quantidade=1, unidade_medida="", categoria="", data_adicao=data,
        ultima_venda="1999-12-24", fornecedor="", observações=""):

    #Adicionando os parâmetros a variáveis
        self.async_engine = create_async_engine(f'postgresql+asyncpg:{conexão}')
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)

    async def Consultar_Estoque(self, campo="codigo_interno", consulta=None):
        try:
            async with self.async_session() as conn:
                inserir_dados = text(f"select descricao, codigo_interno, ean, quantidade from estoque where {campo} = '{consulta}'")
                result = await conn.execute(inserir_dados)
                for row in result:
                    linha = str(row).replace("'", "")
                    with open(r"csv/resultado.csv", "w") as arquivo:
                        arquivo.write(f'descricao,codigo_interno,ean,quantidade\n{self.tratar_resultado_de_consulta(linha)}')
                    df = pd.read_csv(r'csv/resultado.csv')
                    descricao = df['descricao']
                    codigo_interno = df['codigo_interno']
                    if codigo_interno[0] == " ''":
                        codigo_interno = tuple("<desconhecido>")

                    ean = df['ean']
                    quantidade = df['quantidade']
                    return descricao[0], codigo_interno[0], ean[0], quantidade[0]
        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")
        except IntegrityError as e:
            return(f"Violação de integridade: {e}")
        except ConnectionResetError as e:
            return (f"Erro de conexão: {e}")
        except Exception as e:
            return(f"Erro inesperado: {e}")

    async def Atualizar_Estoque(self, quantidade_a_reduzida, código_interno):
        try:
            async with self.async_session() as conn:
                reduzir_estoque = text(f"update estoque set quantidade = quantidade - {quantidade_a_reduzida} where codigo_interno = '{código_interno}';")
                result = await conn.execute(reduzir_estoque, {'quantidade': quantidade_a_reduzida, 'codigo_interno': código_interno})
                await conn.commit()  # Confirma as alterações
                return result

        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")
        except IntegrityError as e:
            return(f"Violação de integridade: {e}")
        except ConnectionResetError as e:
            return (f"Erro de conexão: {e}")
        except Exception as e:
            return(f"Erro inesperado: {e}")



    def tratar_resultado_de_consulta(self, dado):

        self.dado = str(dado)
        return self.dado[1:-1]
            


    

if __name__ == '__main__':
    #adicionando dados
    '''conexao = Conexao()
    resultado = conexao.inserir_dados('Administrador', 'admin', 'admin', 'allmyfilesondrive@gmail.com')
    print(resultado)
'''
    #consultando dados  
    '''   async def main():
        consulta = Query()
        resultado= await consulta.consultar_senha_por_usuario('admin')
        print(resultado)
    asyncio.run(main())'''

    '''async def main():
        cadastrar = Cadastrar_produtos(codigo_interno='123459', descrição='teste', ean='1234567897894', quantidade=4)
        resultado = await cadastrar.inserir_dados()
        print(resultado)
    asyncio.run(main())'''

    '''async def main():
        consultar = consulta()
        resultado = await consultar.Consultar_Estoque(consulta="123458")
        print(resultado)
    asyncio.run(main())'''
    async def main():
        alterar = consulta()
        resultado = await alterar.Atualizar_Estoque(1, '123456')
        print(resultado)
    asyncio.run(main())



