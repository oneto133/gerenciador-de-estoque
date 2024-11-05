from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import OperationalError, IntegrityError
from Funções import Horarios

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
    hora = Horarios()
    data = hora.data_atual()
    def __init__(self, conexão="//postgres:M7cIWJYjxBodNojL@uncertainly-pretty-chimaera.data-1.use1.tembo.io:5432/postgres",
    codigo_interno=None, ean="", descrição="", preco=10.00, quantidade=1, unidade_medida="", categoria="", data_adicao=data,
    ultima_venda="1999-12-24", fornecedor="", observações=""):

    #Adicionando os parâmetros a variáveis
        self.async_engine = create_async_engine(f'postgresql+asyncpg:{conexão}')
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)
        self.codigo_interno = codigo_interno
        self.ean = ean
        self.descrição = descrição
        self.preco = preco
        self.quantidade = quantidade
        self.unidade_medida = unidade_medida
        self.categoria = categoria
        self.data_adicao = data_adicao
        self.ultima_venda = ultima_venda
        self.fornecedor = fornecedor
        self.observações = observações

    async def inserir_dados(self):
        try:
            async with self.async_session() as conn:
                inserir_dados = text("INSERT INTO estoque (codigo_interno, ean, descricao, preco,"
                "quantidade, unidade_medida, categoria, data_adicao, ultima_venda, fornecedor,"
                f"observacoes) VALUES ('{self.codigo_interno}', '{self.ean}', '{self.descrição}', {self.preco}, {self.quantidade},"
                f"'{self.unidade_medida}', '{self.categoria}', '{self.data_adicao}', '{self.ultima_venda}', '{self.fornecedor}',"
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
                inserir_dados = text(f"select * from estoque where {campo} = '{consulta}'")
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
        return self.dado
            


    

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
        cadastrar = Cadastrar_produtos(descrição='teste', ean='1234567897894')
        resultado = await cadastrar.inserir_dados()
        print(resultado)
    asyncio.run(main())'''

    async def main():
        consultar = consulta()
        resultado = await consultar.Consultar_Estoque(campo="descricao", consulta="teste")
        print(resultado)
    asyncio.run(main())

