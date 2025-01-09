import streamlit as st
import pandas as pd
import requests
import os
import base64
import io
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Carrega as variáveis de ambiente
load_dotenv()

username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")
url = os.getenv("API_URL")

st.set_page_config(
    page_title="Abertura Chamados",
    layout="wide",
    initial_sidebar_state="expanded"
)

def chamado():
    # Gerar um DataFrame de exemplo para salvar como .xlsx
    data = {
        'nome': ['Francisco orsi'],
        'email': ['ti.francisco@carmelofior.com.br'],
        'assunto': ['teste modelo'],
        'tipo': ['Solicitação de Serviço'],
        'descricao': ['teste modelo'],
        'anexo': [''],
        'tipoAnexo': [''],
        'planta': ['Matriz'],
        'departamento': ['TI']
    }
    df = pd.DataFrame(data)

    # Converter o DataFrame para bytes em formato .xlsx
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        file_data = buffer.getvalue()

    # Botão de download
    st.download_button(
        label="Baixar arquivo de modelo Excel",
        data=file_data,
        file_name="modelo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Título do aplicativo
    st.title("Upload de Arquivo Excel")

    # Botão para upload do arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xls", "xlsx"])

    # Verifica se um arquivo foi carregado
    if uploaded_file is not None:
        # Lê o arquivo Excel usando pandas
        df = pd.read_excel(uploaded_file)

        # Exibe o DataFrame na tela
        st.write("Dados do arquivo:")
        st.dataframe(df)

        # Converte as colunas para string e substitui valores NaN por uma string vazia
        df = df.astype(str)
        df.fillna('', inplace=True)

        # Converte cada linha do DataFrame em um dicionário
        lista_dicts = df.to_dict(orient='records')

        # Exibe o JSON na tela
        st.write("Dados formatados como JSON:")
        
        # Botão para enviar os dados
        botao = st.button("Abrir Chamados", key="btn_cadastrar")
        
        if botao:  # Verifica se o botão foi clicado
            for item in lista_dicts:
                resultado_json = {
                    "chamado": [
                        {
                            "nome": item.get("nome", ""),
                            "email": item.get("email", ""),
                            "assunto": item.get("assunto", ""),
                            "tipo": item.get("tipo", ""),
                            "descricao": item.get("descricao", ""),
                            "anexo": item.get("anexo", "vazio"),
                            "tipoAnexo": item.get("tipoAnexo", "vazio"),
                            "planta": item.get("planta", ""),
                            "departamento": item.get("departamento", "")
                        }
                    ]
                }

                st.write("Enviando JSON:", resultado_json)  # Exibe o JSON enviado

                # Codifica as credenciais em Base64
                credentials = f"{username}:{password}"
                b64_credentials = base64.b64encode(credentials.encode()).decode()
                headers = {
                    "Authorization": f"Basic {b64_credentials}",
                    "Content-Type": "application/json"  # Adiciona o tipo de conteúdo
                }

                try:
                    response = requests.post(url, json=resultado_json, headers=headers)
                    response.raise_for_status()  # Levanta exceções para códigos de erro HTTP (4xx/5xx)
                    
                    response_data = response.json()  # Tenta obter o JSON completo da resposta da API
                    
                    st.write("Resposta completa da API:", response_data)  # Exibe o conteúdo completo da resposta
                    
                    chamado_id = response_data.get("processo")  # Substitua pela chave correta da API

                    if chamado_id:
                        st.success(f"Dados enviados com sucesso - \nNúmero do Chamado: {chamado_id}")
                    else:
                        st.success(f"Dados enviados com sucesso para: {item.get('nome', '')}")

                except requests.exceptions.HTTPError as http_err:
                    st.error(f"Erro HTTP ao enviar dados para {item.get('nome', '')}: {http_err}")
                    st.write("Código de erro:", response.status_code)
                    st.write("Mensagem de erro:", response.text)  # Exibe detalhes da mensagem de erro
                except Exception as e:
                    st.error(f"Ocorreu um erro ao enviar dados para {item.get('nome', '')}: {e}")


def chamado_rbackup():

    rbackup = st.button("Restore Backup")

    # Definir o mês e ano atual
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    # Calcular o número de semanas no mês atual
    last_day = datetime(current_year, current_month+1, 1) - timedelta(days=1)
    num_weeks = (last_day.day - 1) // 7 + 1

    # Criar as listas de meses e semanas
    months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    weeks = [f'Semana {i+1}' for i in range(num_weeks)]

    # Criar o DataFrame
    data = []
    for plant in ['Matriz', 'Pisoforte', 'Serra Azul']:
        for week in range(num_weeks):
            data.append({
                'Solicitante': 'Francisco Orsi',
                'Planta': plant,
                'Assunto': f'Restore backup - {weeks[week]} - {months[current_month-1]}/{current_year}',
                'Tipo': 'Solicitação de Serviço',
                'Descrição': f'Restore backup - {weeks[week]} - {months[current_month-1]}/{current_year}',
                'anexo': '',
                'tipoAnexo': '',
                'planta': plant,
                'departamento': 'TI'
            })
    

    if rbackup:
            st.write("Dados do arquivo:")
            edited_data = st.data_editor(data, num_rows="dynamic")
    
    return pd.DataFrame(data)
        

# Sidebar
st.sidebar.title("Opções")
selected_option = st.sidebar.radio("Selecione uma opção", ["Enviar vários chamados", "Gerar Chamados Restore Backup"])

if selected_option == "Enviar vários chamados":
    chamado()
elif selected_option == "Gerar Chamados Restore Backup":
    chamado_rbackup()
