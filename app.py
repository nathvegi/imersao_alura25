import streamlit as st
from typing import Union, List
import google.generativeai as genai
from PIL import Image
import io
import os

# --- CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA CHAMADA DO ST. NO SCRIPT) ---
st.set_page_config(
    page_title="DescreveAI - Transforme imagens em vendas com inteligência artificial",
    page_icon="assets/favicon.png", # Altere para o caminho e nome do seu arquivo favicon!
    layout="centered", # ou "wide" para ocupar mais espaço na tela
    initial_sidebar_state="auto" # "auto", "expanded", ou "collapsed"
)
# --- FIM DA CONFIGURAÇÃO DA PÁGINA ---

# Configuração da API KEY do Google Gemini (use st.secrets) - PRIMEIRO E ÚNICO BLOCO DE INICIALIZAÇÃO
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # --- MENSAGENS DE BOAS-VINDAS E INSTRUÇÕES ---
    st.sidebar.markdown("### Boas-vindas ao DescreveAI - v 1.0.8! 👋")
    st.sidebar.markdown(
        """
        Dê vida aos **produtos para o seu e-commerce**! Sou seu assistente inteligente, 
        pronto para transformar as imagens dos seus produtos em **descrições impactantes**, 
        totalmente otimizadas para vendas e visibilidade em mecanismos de busca (SEO). 
        Tudo isso com o poder da inteligência artificial do Google Gemini.

        **Como é fácil usar:**
        1.  **Carregue a imagem** (aquela que você já usa no seu e-commerce!) clara e de boa qualidade do seu produto.
        2.  (Opcional) Adicione **detalhes adicionais** importantes sobre o produto (material, marca, público-alvo, funcionalidades, etc.).
        3.  Clique em **"Gerar Descrição"** e prepare-se para a mágica! 🧙🏼‍♂️

        Simplifique sua rotina e impulsione suas vendas. Comece agora!
        """
    )
    st.sidebar.markdown("---") # Adiciona uma linha divisória para separar
    st.sidebar.markdown("Created by **NathVegi**") # Sua assinatura!    
    # --- FIM DAS MENSAGENS DE BOAS-VINDAS ---

    # MENSAGEM DE STATUS DO SISTEMA QUANDO ONLINE
    st.sidebar.success("Status do Sistema: 🟢 Online") # Status do Sistema

    # st.sidebar.success("API Key carregada com sucesso!") # Linha de debug comentada
    # st.sidebar.info(f"Comprimento da API Key: {len(GOOGLE_API_KEY) if GOOGLE_API_KEY else 0}") # Linha de debug comentada

except Exception as e:
    # MENSAGEM DE STATUS DO SISTEMA QUANDO OFFLINE
    st.sidebar.error("Status do Sistema: 🔴 Offline. Por favor, tente novamente mais tarde. Caso o erro persista, entre em contato com o suporte: natvegi@gmail.com")
    st.sidebar.info(f"Detalhes do erro: {e}") # Opcional: manter detalhes do erro para debug, mas pode ser removido em produção
    st.stop() # Interrompe a execução se a chave não for carregada

    # --- INTERFACE STREAMLIT PRINCIPAL ---
    # LINHA DO TÍTULO REMOVIDA/COMENTADA
    # st.title("DescreveAI: Descrições de Produtos Inteligentes") 

# --- IMAGEM DA LOGO NO CORPO PRINCIPAL (CENTRALIZADA) ---

# Crie três colunas: a primeira e a última vazias, a do meio para a imagem
# A proporção [1, 2, 1] é um bom ponto de partida para centralizar.
# A coluna do meio (2) terá o dobro do tamanho das laterais (1).
col1, col2, col3 = st.columns([1, 2, 1]) 

with col2: # Todo o conteúdo dentro deste 'with' será colocado na coluna do meio
    st.image("assets/logo_descreveai.png", use_container_width=True) # Mantenha seu 'width=550' aqui ou ajuste conforme desejar.
    
st.markdown("---") # Adiciona uma linha divisória abaixo da logo para separar o conteúdo
# --- FIM DA IMAGEM DA LOGO NO CORPO PRINCIPAL ---

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
            return "Erro interno: Falha ao carregar a imagem para o modelo."

    if not parts:
        st.warning("call_gemini_model: Nenhuma entrada fornecida para o modelo.")
        return "Nenhuma entrada válida para o modelo."

    try:
        response = model.generate_content(parts)

        if response and hasattr(response, 'text') and response.text is not None:
            return response.text
        else:
            st.error("call_gemini_model: A API retornou uma resposta inesperada (vazia ou sem atributo 'text').")
            return "Erro: Resposta vazia ou inesperada do modelo Gemini."

    except Exception as e:
        st.error(f"call_gemini_model: Erro na chamada do modelo Gemini: {e}")
        st.exception(e)
        return "Erro: Falha na comunicação com o modelo Gemini."

##########################################
# --- Agente 1: Analista de Imagem --- #
##########################################
def agente_imagem(imagem_produto_bytes):
    analista_imagem_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        generation_config=genai.GenerationConfig(temperature=0.4),
        system_instruction="""
        Você é um agente especializado na descrição de imagens de produtos para e-commerce, com foco exclusivo em vestuário de dormir (como pijamas, camisolas, short doll, robes, etc.). Sua tarefa é analisar a imagem de um produto e descrever suas características visuais principais, de forma concisa e objetiva.

        Para a descrição, considere os seguintes aspectos:

        1 - Características do vestuário:
           - Tipo de peça de dormir (ex: pijama, camisola, short doll, robe).
           - Cor(es) predominante(s) e secundárias.
           - Formato/modelagem (ex: justo, solto, longo, curto, regata, manga longa, manga curta, decote V, gola redonda).
           - Material aparente/textura (ex: algodão, seda, liganete, malha, flanela, cetim, liso, texturizado, com brilho).
           - Detalhes de design (ex: botões, zíperes, rendas, laços, bolsos).
           - Quaisquer outros detalhes relevantes para a identificação do produto.
        
        2 - Informações demográficas (se aplicável):
            - Se o produto é adulto ou infantil.
            - Se o produto é feminino ou masculino.
        
        3 - Exclusões:
            - Não descreva o que o modelo está calçando. O foco é exclusivamente na roupa de dormir.
            - Evite descrições subjetivas ou opinativas (ex: "bonito", "confortável", "elegante").
            - Mantenha a descrição objetiva e factual.
            - NÃO DESCREVA EM HIPÓTESE ALGUMA: bordados E inscrições das estampas.
            - A descrição deve ser concisa e direta, listando as características principais de forma clara e organizada.

        Exemplo de saída esperada:

        'Pijama infantil feminino, cor rosa com estampa de unicórnios, modelagem solta de manga curta, material de algodão macio. Possui botões frontais e gola redonda.'

        Agora, proceda com a análise da imagem do produto.
        """
    )
    # st.info("Agente Imagem: Chamando o modelo para análise da imagem...") # Linha de debug comentada
    caracteristicas_visuais = call_gemini_model(analista_imagem_model, image_bytes=imagem_produto_bytes, message_text="Por favor, descreva esta imagem:")
    # st.info(f"Agente Imagem: Características visuais obtidas (primeiros 50 chars): '{caracteristicas_visuais[:50] if caracteristicas_visuais else 'Vazio'}'") # Linha de debug comentada
    return caracteristicas_visuais

#######################################################
# --- Agente 2: Analista de Texto e Enriquecimento --- #
#######################################################
def agente_analista_texto(caracteristicas_visuais, info_textual_adicional):
    analista_texto_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        generation_config=genai.GenerationConfig(temperature=0.7),
        system_instruction="""
        Você é um Analista de Imagem Enriquecido e Redator de Descrições para o e-commerce Useveggi, especializado em vestuário de dormir.

        Sua tarefa é criar uma descrição completa e detalhada do produto para o site da Useveggi, combinando inteligentemente duas fontes de informação:
        
        1 - As características visuais do produto (fornecidas anteriormente por um agente de imagem).
        2 - As informações textuais adicionais (fornecidas pelo usuário, que podem incluir detalhes como composição do tecido, tecnologias, instruções de cuidado, diferenciais de conforto, etc.).
        
        Para a elaboração da descrição:
        
        - Integração Coesa: Assegure que todos os detalhes visuais e textuais sejam harmoniosamente incorporados, formando um texto único, coeso e informativo.
        - Valorização de Detalhes Não-Visíveis: Dê especial atenção e destaque a informações que não são perceptíveis apenas pela imagem, mas que foram mencionadas nos dados textuais.
        - Linguagem Fluida e Focada no Cliente: Formule uma descrição contínua, natural e fácil de ler, que ajude o cliente da Useveggi a entender o produto de forma abrangente e atraente, sempre alinhada ao tom da marca de vestuário de dormir.
        - Relevância para Vestuário de Dormir: Mantenha a descrição focada nos atributos e benefícios mais importantes para produtos de dormir (ex: conforto, respirabilidade, durabilidade, caimento, sensibilidade da pele, etc.).

        Exclusões:
        - NÃO DESCREVA EM HIPÓTESE ALGUMA: bordados E inscrições das estampas, SALVO EXCEÇÕES ONDE ESTES DETALHES FOREM INFORMADOS PELO USUÁRIO NAS INFORMAÇÕES TEXTUAIS.
        
        Você receberá as informações da seguinte forma:
        
        Características Visuais:
        [Descrição visual gerada pelo agente de imagem]
        
        Informações Textuais Adicionais:
        [Texto com detalhes suplementares fornecidos pelo usuário]
        
        Com base nessas duas fontes, crie a descrição detalhada do produto.
        """
    )
    entrada_do_agente_analista_texto = f"""
    Características Visuais: {caracteristicas_visuais}

    Informações Textuais Adicionais: {info_textual_adicional}

    Por favor, crie uma descrição enriquecida do produto com base nessas informações.
    """
    # st.info("Agente Analista Texto: Chamando o modelo para enriquecimento...") # Linha de debug comentada
    descricao_enriquecida = call_gemini_model(analista_texto_model, message_text=entrada_do_agente_analista_texto)
    # st.info(f"Agente Analista Texto: Descrição enriquecida (primeiros 50 chars): '{descricao_enriquecida[:50] if descricao_enriquecida else 'Vazio'}'") # Linha de debug comentada
    return descricao_enriquecida

################################################################
# --- Agente 3: Otimizador de SEO e Redator de Descrições --- #
################################################################
def agente_otimizador_redator(descricao_preliminar):
    otimizador_redator_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        generation_config=genai.GenerationConfig(temperature=0.8),
        system_instruction="""
        Você é um Analista Otimizador de SEO, Palavras-Chave, Meta Tags e Redator de Descrições, especializado em e-commerce e focado em vendas online, com um profundo conhecimento de otimização para plataformas como a VTEX Legacy. Seu trabalho é gerar descrições e palavras-chave para o site da Useveggi.

        Sua principal tarefa é pegar uma descrição preliminar de um produto e transformá-la em uma descrição altamente otimizada para SEO e vendas online. Além disso, você deve identificar e gerar um conjunto de palavras-chave específicas para a busca interna do e-commerce (VTEX Legacy).

        Para otimizar a descrição:

        1 - Análise Aprofundada: Analise a descrição preliminar para compreender o produto, suas características, nicho de mercado e público-alvo, considerando o estilo e o público da Useveggi.
        2 - Identificação de Palavras-Chave: Pense em termos de busca de cauda longa e curta que clientes reais utilizariam para encontrar este produto, tanto em motores de busca (Google, etc.) quanto dentro do e-commerce Useveggi. Gere apenas as palavras-chave principais e mais relevantes que identifiquem o produto, com foco em qualidade, não em quantidade.
        3 - Incorporação Estratégica: Incorpore essas palavras-chave de forma natural e fluida ao longo da descrição, priorizando a inserção nas primeiras frases e no título (se aplicável).
        4 - Foco em Benefícios e Soluções: Utilize linguagem persuasiva e focada nos benefícios para o cliente. Destaque como o produto resolve problemas, atende necessidades ou agrega valor à vida do consumidor.
        5 - NUNCA FAÇA uma descrição Literal de Estampas: A descrição deve complementar a imagem, não substituí-la para quem não pode vê-la.
        6 - Concisão e Legibilidade: Mantenha a descrição concisa, fácil de ler e atraente. Evite bullet points. Priorize frases curtas e diretas, quando apropriado.
        7 - Restrição de Linguagem Infantil: Em produtos infantis, NÃO utilize expressões como "para a pequena", "para o pequeno", "para sua pequena", "para seu pequeno" ao se referir a crianças. Mantenha uma linguagem neutra e inclusiva.
        
        Formato de Saída:

        A sua entrega deve ser estruturada da seguinte forma:

        1 - Descrição Otimizada para SEO e Vendas: O texto final da descrição do produto.
        2 - Palavras-Chave para Busca Interna (VTEX Legacy): Uma lista de aproximadamente 10 palavras-chave (não mais que 15), principais e relevantes que identifiquem o produto, separadas por vírgula e sem espaço após cada vírgula, listadas na linha seguinte à descrição otimizada. Exemplo: palavrachave1,palavrachave2,palavrachave3
        
        Agora, proceda com a otimização com base na descrição preliminar que será fornecida.
            """
    )
    entrada_do_agente_otimizador_redator = f"""
    Descrição Preliminar: {descricao_preliminar}

    Por favor, otimize esta descrição para SEO e vendas online.
    """
    # st.info("Agente Otimizador: Chamando o modelo para otimização...") # Linha de debug comentada
    descricao_otimizada = call_gemini_model(otimizador_redator_model, message_text=entrada_do_agente_otimizador_redator)
    # st.info(f"Agente Otimizador: Descrição otimizada (primeiros 50 chars): '{descricao_otimizada[:50] if descricao_otimizada else 'Vazio'}'") # Linha de debug comentada
    return descricao_otimizada

# Interface Streamlit Principal
# st.title("DescreveAI: Descrições de Produtos Inteligentes")

# Esta seção foi movida e integrada ao primeiro bloco de inicialização da API acima
# with st.sidebar:
#     st.subheader("Configuração da API")
#     st.info("Certifique-se de ter sua `GOOGLE_API_KEY` configurada em `.streamlit/secrets.toml`")


uploaded_file = st.file_uploader("Carregue a imagem do produto", type=["jpg", "jpeg", "png"])
additional_text = st.text_area("Informações adicionais sobre o produto (opcional)")

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Imagem do Produto Carregada.", use_container_width=True)

    if st.button("Gerar Descrição"):
        st.info("Iniciando a geração da descrição...") # Esta é uma mensagem de progresso, não de debug, pode manter se quiser

        descricao_final = "" # Inicializa com string vazia

        # CHAMADA DO AGENTE 1
        with st.spinner("Analisando a imagem..."):
            imagens_analisadas = agente_imagem(image_bytes)
            # st.info(f"DEBUG: Valor de imagens_analisadas: '{imagens_analisadas[:50] if imagens_analisadas else 'Vazio'}'") # Linha de debug comentada
            # EXIBIR O RESULTADO DO AGENTE 1
            if imagens_analisadas:
                st.subheader("1. Análise da Imagem:")
                st.write(imagens_analisadas)
            else:
                st.error("Falha na análise da imagem. Descrição não gerada.")
                st.stop()

        # CHAMADA DO AGENTE 2
        with st.spinner("Enriquecendo a descrição..."):
            descricao_imagem = agente_analista_texto(imagens_analisadas, additional_text)
            # st.info(f"DEBUG: Valor de descricao_imagem: '{descricao_imagem[:50] if descricao_imagem else 'Vazio'}'") # Linha de debug comentada
            # EXIBIR O RESULTADO DO AGENTE 2
            if descricao_imagem:
                st.subheader("2. Descrição Enriquecida (com informações textuais):")
                st.write(descricao_imagem)
            else:
                st.error("Falha ao enriquecer a descrição. Descrição não gerada.")
                st.stop()

        # CHAMADA DO AGENTE 3
        with st.spinner("Otimizando para SEO..."):
            descricao_final = agente_otimizador_redator(descricao_imagem)
            # st.info(f"DEBUG: Valor de descricao_final ANTES DO st.write: '{descricao_final[:50] if descricao_final else 'Vazio'}'") # Linha de debug comentada
            # EXIBIR O RESULTADO DO AGENTE 3 (A DESCRIÇÃO FINAL)
            if descricao_final:
                st.subheader("3. Descrição Final: Otimizada para SEO e Vendas:")
                # Prova dos 9 (ainda mantida para segurança, mas você pode remover essa verificação agora)
                if "AIzaSy" in descricao_final and "GOOGLE_API_KEY" in descricao_final:
                    st.error("ERRO GRAVE: A API Key está sendo exibida na descrição final.")
                    st.code(f"Conteúdo da descricao_final: {descricao_final}")
                    st.write("Isso indica um problema de fluxo de dados ou atribuição. Verifique logs do Streamlit Cloud.")
                else:
                    st.write(descricao_final) # Exibe a descrição otimizada
            else:
                st.error("Falha ao otimizar a descrição para SEO. Descrição não gerada.")
                st.stop()

        st.success("Processo de geração de descrição concluído!")

else:
    st.info("Por favor, carregue uma imagem do produto para começar.")
