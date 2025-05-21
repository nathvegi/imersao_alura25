import streamlit as st
from typing import Union, List
import google.generativeai as genai
from PIL import Image
import io
import os

# Configuração da API KEY do Google Gemini (use st.secrets)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    st.sidebar.success("API Key carregada com sucesso!") # Feedback visual
    st.sidebar.info(f"Comprimento da API Key: {len(GOOGLE_API_KEY) if GOOGLE_API_KEY else 0}") # Depuração de comprimento
except Exception as e:
    st.sidebar.error(f"Erro ao carregar API Key: {e}") # Feedback visual
    st.stop() # Interrompe a execução se a chave não for carregada

# Função utilitária para chamar o modelo Gemini
def call_gemini_model(model: genai.GenerativeModel, image_bytes: Union[bytes, None] = None, message_text: Union[str, None] = None) -> str:
    parts = []
    if message_text:
        parts.append(message_text)
    if image_bytes:
        try:
            image_pil = Image.open(io.BytesIO(image_bytes))
            parts.append(image_pil)
        except Exception as e:
            st.error(f"Erro ao processar imagem para o Gemini: {e}")
            return "Erro interno: Falha ao carregar a imagem para o modelo." # Nunca retornar a chave aqui

    if not parts:
        st.warning("call_gemini_model: Nenhuma entrada fornecida para o modelo.")
        return "Nenhuma entrada válida para o modelo." # Nunca retornar a chave aqui

    try:
        response = model.generate_content(parts)

        # Verificação robusta da resposta
        if response and hasattr(response, 'text') and response.text is not None:
            return response.text
        else:
            st.error("call_gemini_model: A API retornou uma resposta inesperada (vazia ou sem atributo 'text').")
            # Em caso de resposta vazia ou estranha, retorna uma mensagem de erro, NUNCA A API KEY
            return "Erro: Resposta vazia ou inesperada do modelo Gemini."

    except Exception as e:
        st.error(f"call_gemini_model: Erro na chamada do modelo Gemini: {e}")
        st.exception(e) # Exibe o traceback completo no Streamlit
        # Em caso de qualquer erro na chamada da API, retorna uma string de erro, NUNCA A API KEY
        return "Erro: Falha na comunicação com o modelo Gemini."

##########################################
# --- Agente 1: Analista de Imagem --- #
##########################################
def agente_imagem(imagem_produto_bytes):
    analista_imagem_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Mantenha este. Se quiser testar o "2.5 Flash", terá que ser via API e verificar compatibilidade.
        generation_config=genai.GenerationConfig(temperature=0.4),
        system_instruction="""
        Você é um agente de imagem. A sua tarefa é analisar a imagem deste produto e descrever suas características visuais principais,
        incluindo cor, formato, material aparente e quaisquer detalhes de design ou textura.
        Liste as características de forma concisa. Você deve ignorar o que o modelo estiver calçando, porque o produto a ser vendido é apenas o pijama.
        Você precisa considerar se o modelo é adulto ou infantil, feminino ou masculino para informar que o produto é adulto ou infantil, feminino ou masculino.
        """
    )
    st.info("Agente Imagem: Chamando o modelo para análise da imagem...") # Depuração
    caracteristicas_visuais = call_gemini_model(analista_imagem_model, image_bytes=imagem_produto_bytes, message_text="Por favor, descreva esta imagem:")
    st.info(f"Agente Imagem: Características visuais obtidas (primeiros 50 chars): '{caracteristicas_visuais[:50] if caracteristicas_visuais else 'Vazio'}'") # Depuração
    return caracteristicas_visuais

#######################################################
# --- Agente 2: Analista de Texto e Enriquecimento --- #
#######################################################
def agente_analista_texto(caracteristicas_visuais, info_textual_adicional):
    analista_texto_model = genai.GenerativeModel(
        model_name="gemini-pro", # Use "gemini-pro" ou "gemini-1.5-flash" para texto
        generation_config=genai.GenerationConfig(temperature=0.7),
        system_instruction="""
        Você é um analista de imagem enriquecido. Sua tarefa é combinar as características visuais do produto,
        fornecidas anteriormente, com as informações textuais adicionais, fornecidas pelo usuário.
        Use ambas as fontes de informação para criar uma descrição completa e detalhada do produto.
        Inclua detalhes que não eram visíveis apenas na imagem, mas que foram mencionados nas informações textuais.
        Formule uma descrição fluida e informativa que combine todos os dados disponíveis.
        """
    )
    entrada_do_agente_analista_texto = f"""
    Características Visuais: {caracteristicas_visuais}

    Informações Textuais Adicionais: {info_textual_adicional}

    Por favor, crie uma descrição enriquecida do produto com base nessas informações.
    """
    st.info("Agente Analista Texto: Chamando o modelo para enriquecimento...") # Depuração
    descricao_enriquecida = call_gemini_model(analista_texto_model, message_text=entrada_do_agente_analista_texto)
    st.info(f"Agente Analista Texto: Descrição enriquecida (primeiros 50 chars): '{descricao_enriquecida[:50] if descricao_enriquecida else 'Vazio'}'") # Depuração
    return descricao_enriquecida

################################################################
# --- Agente 3: Otimizador de SEO e Redator de Descrições --- #
################################################################
def agente_otimizador_redator(descricao_preliminar):
    otimizador_redator_model = genai.GenerativeModel(
        model_name="gemini-pro", # Use "gemini-pro" ou "gemini-1.5-flash" para texto
        generation_config=genai.GenerationConfig(temperature=0.8),
        system_instruction="""
        Você é um Analista Otimizador de SEO e Redator de Descrições especializado em e-commerce.
        Sua tarefa é pegar a descrição preliminar de um produto e otimizá-la para vendas online e motores de busca (SEO).

        Para otimizar a descrição:
        1. Analise a descrição preliminar para entender o produto e suas características.
        2. Pense em palavras-chave relevantes que os clientes usariam para buscar este tipo de produto online.
        3. Incorpore naturalmente essas palavras-chave ao longo da descrição, especialmente no início.
        4. Use linguagem persuasiva focada nos benefícios para o cliente. Destaque como o produto resolve um problema ou atende a uma necessidade.
        5. Mantenha a descrição concisa e fácil de ler. Não use bullet points e gere frases curtas se apropriado.

        Crie a descrição otimizada para SEO e vendas.
            """
    )
    entrada_do_agente_otimizador_redator = f"""
    Descrição Preliminar: {descricao_preliminar}

    Por favor, otimize esta descrição para SEO e vendas online.
    """
    st.info("Agente Otimizador: Chamando o modelo para otimização...") # Depuração
    descricao_otimizada = call_gemini_model(otimizador_redator_model, message_text=entrada_do_agente_otimizador_redator)
    st.info(f"Agente Otimizador: Descrição otimizada (primeiros 50 chars): '{descricao_otimizada[:50] if descricao_otimizada else 'Vazio'}'") # Depuração
    return descricao_otimizada

# Interface Streamlit
st.title("DescreveAI: Descrições de Produtos Inteligentes")

# Configuração da chave de API usando st.secrets (já movido para cima para feedback inicial)
with st.sidebar:
    st.subheader("Configuração da API")
    st.info("Certifique-se de ter sua `GOOGLE_API_KEY` configurada em `.streamlit/secrets.toml`")


uploaded_file = st.file_uploader("Carregue a imagem do produto", type=["jpg", "jpeg", "png"])
additional_text = st.text_area("Informações adicionais sobre o produto (opcional)")

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Imagem do Produto Carregada.", use_container_width=True)

    if st.button("Gerar Descrição"):
        st.info("Iniciando a geração da descrição...")

        descricao_final = "" # Inicializa com string vazia

        # CHAMADA DO AGENTE 1
        with st.spinner("Analisando a imagem..."):
            imagens_analisadas = agente_imagem(image_bytes)
            st.info(f"DEBUG: Valor de imagens_analisadas: '{imagens_analisadas[:50] if imagens_analisadas else 'Vazio'}'")
            if not imagens_analisadas or "Erro" in imagens_analisadas: # Adicionado check para "Erro"
                st.error("Falha na análise da imagem. Descrição não gerada.")
                st.stop() # Parar aqui se houver falha

        # CHAMADA DO AGENTE 2
        with st.spinner("Enriquecendo a descrição..."):
            descricao_imagem = agente_analista_texto(imagens_analisadas, additional_text)
            st.info(f"DEBUG: Valor de descricao_imagem: '{descricao_imagem[:50] if descricao_imagem else 'Vazio'}'")
            if not descricao_imagem or "Erro" in descricao_imagem: # Adicionado check para "Erro"
                st.error("Falha ao enriquecer a descrição. Descrição não gerada.")
                st.stop()

        # CHAMADA DO AGENTE 3
        with st.spinner("Otimizando para SEO..."):
            descricao_final = agente_otimizador_redator(descricao_imagem)
            st.info(f"DEBUG: Valor de descricao_final ANTES DO st.write: '{descricao_final[:50] if descricao_final else 'Vazio'}'")
            if not descricao_final or "Erro" in descricao_final: # Adicionado check para "Erro"
                st.error("Falha ao otimizar a descrição para SEO. Descrição não gerada.")
                st.stop() # Parar aqui se houver falha

        st.success("Processo de geração de descrição concluído!")

        st.subheader("Descrição Final Gerada:")
        # AGORA, A PROVA DOS 9:
        if "AIzaSy" in descricao_final and "GOOGLE_API_KEY" in descricao_final:
            st.error("ERRO GRAVE: A API Key está sendo exibida na descrição final.")
            st.code(f"Conteúdo da descricao_final: {descricao_final}") # Mostra o conteúdo exato
            st.write("Isso indica um problema de fluxo de dados ou atribuição. Verifique logs do Streamlit Cloud.")
        elif descricao_final:
            st.write(descricao_final)
        else:
            st.warning("Nenhuma descrição final foi gerada.")


else:
    st.info("Por favor, carregue uma imagem do produto para começar.")
