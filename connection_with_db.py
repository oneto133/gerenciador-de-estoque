from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import OperationalError, IntegrityError
from Funções import Horarios
import pandas as pd
from sqlalchemy import select, text
import asyncio, os, csv
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime


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
    ultima_venda="1999-12-24", fornecedor="", observações="", rua=int(), modulo=int(), nivel=int()):
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
                f"observacoes, rua, modulo, nivel) VALUES ('{self.codigo_interno}', '{self.ean}', '{self.descrição}', {self.preco}, {self.quantidade},"
                f"'{self.unidade_medida}', '{self.categoria}', '{self.data}', '{self.ultima_venda}', '{self.fornecedor}',"
                f"'{self.observações}', {int(rua)}, {int(modulo)}, {int(nivel)})")
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
        campo_de_pesquisa = campo
        consulta = consulta
        if consulta.strip().isalpha():
            campo_de_pesquisa = "descricao"
        consultar = {
            'codigo': f"select descricao, codigo_interno, ean, quantidade, rua, modulo, nivel from estoque where {campo_de_pesquisa} like '%{consulta}%';"
        }
        try:
            async with self.async_session() as conn:
                inserir_dados = text(consultar['codigo'])
                result = await conn.execute(inserir_dados)
                for row in result:
                    linha = str(row).replace("'", "")
                    with open(r"csv/resultado.csv", "w") as arquivo:
                        arquivo.write(f'descricao,codigo_interno,ean,quantidade,rua,modulo,nivel\n{self.tratar_resultado_de_consulta(linha)}')
                    df = pd.read_csv(r'csv/resultado.csv')
                    descricao = df['descricao']
                    codigo_interno = df['codigo_interno']
                    if codigo_interno[0] == " ''":
                        codigo_interno = tuple("<desconhecido>")

                    ean = df['ean']
                    quantidade = df['quantidade']
                    rua = df['rua']
                    modulo = df['modulo']
                    nivel = df['nivel']
                    return descricao[0], codigo_interno[0], ean[0], quantidade[0], rua[0], modulo[0], nivel[0]
        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")
        except IntegrityError as e:
            return(f"Violação de integridade: {e}")
        except ConnectionResetError as e:
            return (f"Erro de conexão: {e}")
        except Exception as e:
            return(f"Erro inesperado: {e}")

    async def Atualizar_Estoque(self,codigo_interno, quantidade_a_ser_reduzida, número_do_pedido, tipo="Faturamento", observacoes=None):
        try:
            async with self.async_session() as conn:
                reduzir_estoque = text(f"update estoque set quantidade = quantidade - {quantidade_a_ser_reduzida} where codigo_interno = '{codigo_interno}';")
                resultado = await conn.execute(reduzir_estoque)

                Faturamento = text(f"insert into faturammento (codigo_interno, quantidade, tipo, pedido, observacoes) values ('{codigo_interno}', {quantidade_a_ser_reduzida}, '{tipo}', '{número_do_pedido}', '{observacoes}');")
                result = await conn.execute(Faturamento)

                await conn.commit()  # Confirma as alterações
                return result, resultado

        except OperationalError as e:
            return(f"Erro de conexão ou sintaxe SQL: {e}")
        except IntegrityError as e:
            return(f"Violação de integridade: {e}")
        except ConnectionResetError as e:
            return (f"Erro de conexão: {e}")
        except Exception as e:
            return(f"Erro inesperado: {e}")

    async def Faturamento(self, código_interno, quantidade=int(1), tipo="Faturamento", número_do_pedido=None, observações=None):
        try:
            async with self.async_session() as conn:
                reduzir_estoque = text(f"insert into faturamento (codigo_interno, quantidade, tipo, numero_do_pedido) values '{codigo_interno}', {quantidade}, {tipo}, {número_do_pedido};")
                result = await conn.execute(reduzir_estoque)
                await conn.commit()  # Confirma as alterações
                return result
        
        except Exception as e:
            print(e)


    async def relatorio(self, destino, tipo, código_interno=str(),
    data_inicio=str(), data_fim=str(), tipo_de_movimentação="Faturamento", abrir=0):

        strings = {
            "consulta": (
                "SELECT codigo_interno, quantidade, pedido, tipo, observacoes FROM faturammento WHERE"
                f" codigo_interno = '{código_interno}' AND data_adicao BETWEEN '{data_inicio}' AND '{data_fim}'"
                f" AND tipo = '{tipo_de_movimentação}';"
            ),
            "None": (
                f"Nenhum resultado a ser retornado quanto ao {tipo_de_movimentação} ou ao período entre {data_inicio} "
                f"e {data_fim}"
            ),
            "destino/caminho": f"{destino}/relatorio_estoque.{tipo}",
            "sucesso!": f"Relatório gerado com sucesso em {destino}/relatorio_estoque.{tipo}"
        }
        try:
            async with self.async_session() as session:
                result = await session.execute(text(strings['consulta']))
                rows = result.fetchall()
                columns = result.keys()
                if len(rows) == 0:
                    return strings['None']
                df = pd.DataFrame(rows, columns=columns)

                if tipo == "xlsx":
                    df.to_excel(strings['destino/caminho'], index=False)
                    return strings['sucesso!']

                elif tipo == "csv":
                    df.to_csv(strings['destino/caminho'], index=False, encoding="utf-8")
                    return strings['sucesso!']
                
                elif tipo == "pdf":
                    try:
                        c = canvas.Canvas(strings['destino/caminho'], pagesize=letter)
                        largura, altura = letter  # Tamanho da página

                        # Definir as margens e altura inicial
                        margem_esquerda = 50
                        margem_superior = altura - 50
                        altura_linha = 14  # Altura de cada linha

                        # Escrever o título
                        c.setFont("Helvetica-Bold", 14)
                        c.drawString(margem_esquerda, margem_superior, "Relatório - Dados")

                        # Escrever os cabeçalhos das colunas
                        c.setFont("Helvetica-Bold", 9)
                        y = margem_superior - 30  # Ajustar a posição vertical
                        for col in columns:
                            c.drawString(margem_esquerda, y, col)
                            margem_esquerda += 90  # Espaço entre as colunas

                        # Escrever os dados
                        c.setFont("Helvetica", 8)
                        for index, row in df.iterrows():
                            margem_esquerda = 50  # Resetar para a posição inicial
                            y -= altura_linha  # Mover para a linha abaixo
                            for valor in row:
                                c.drawString(margem_esquerda, y, str(valor))
                                margem_esquerda += 90  # Espaço entre as colunas
                            if y <= 50:  # Verifica se chegou no final da página
                                c.showPage()  # Adiciona uma nova página
                                c.setFont("Helvetica-Bold", 10)
                                y = altura - 50  # Reseta a altura para o topo

                        # Finalizar o PDF
                        c.save()
                        return strings['sucesso!']
                    except Exception as e:
                        return e
                

        except Exception as e:
            return f"Erro ao gerar relatório: {e}"

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
    '''async def main():
        alterar = consulta()
        resultado = await alterar.Atualizar_Estoque(codigo_interno='123456', quantidade_a_ser_reduzida=1,número_do_pedido='1234567891')
        print(resultado)
    asyncio.run(main())'''

    async def main():
        consultar = consulta()
        resultado = await consultar.relatorio()

    asyncio.run(main())



