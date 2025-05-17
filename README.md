# 🚀✨ Descrições de Produtos Turbinadas com SEO e IA: Seu Catalisador de Vendas Inteligente! ✨🚀

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1QnBrHB6y1PXzuUjtzIRS7HUFsYJBxWJs?usp=sharing)
![Project Demo](link\_para\_um\_gif\_ou\_screenshot\_do\_projeto\_em\_acao\_aqui)

Este projeto inovador apresenta um sistema de três agentes de Inteligência Artificial, alimentados pela poderosa API Gemini, projetado para revolucionar a forma como as descrições de produtos são criadas e otimizadas para o e-commerce. Meu objetivo é fornecer descrições não apenas informativas, mas também altamente atraentes para os clientes e perfeitamente alinhadas com as melhores práticas de SEO, impulsionando a visibilidade e as vendas online.

## 💡 A Ideia por Trás do Projeto

No competitivo mundo do e-commerce, descrições de produtos de alta qualidade são essenciais para converter visitantes em compradores. Este sistema automatiza e aprimora esse processo, aproveitando a visão computacional e o processamento de linguagem natural de modelos de IA de ponta para:

* **Capturar a Essência Visual:** Analisar imagens de produtos para identificar detalhes cruciais que muitas vezes se perdem em descrições genéricas.
* **Enriquecer com Contexto Humano:** Integrar informações adicionais fornecidas pelo usuário, adicionando nuances e detalhes específicos que a imagem sozinha não revela.
* **Conquistar os Mecanismos de Busca:** Otimizar o texto gerado com palavras-chave estratégicas e uma linguagem persuasiva, elevando o potencial de descoberta do produto.

## ✨ Funcionalidades que Impulsionam Vendas

* **👁️ Análise Visual Inteligente:** O `agente_imagem` mergulha na imagem do seu produto, desvendando cores vibrantes, formatos distintos, materiais aparentes e detalhes de design que cativam o olhar do cliente.
* **✍️ Enriquecimento Textual Humano-IA:** O `agente_analista_texto` harmoniza a precisão da análise visual com a riqueza das informações textuais fornecidas pelo usuário, criando descrições completas e envolventes que contam a história do seu produto.
* **🎯 Otimização Estratégica para SEO:** Nos bastidores, o sistema aplica princípios de SEO para garantir que cada descrição não apenas informe, mas também atraia tráfego orgânico qualificado, colocando seus produtos no topo dos resultados de busca.
* **🔒 Entrada de Imagem Robusta:** Priorizamos a qualidade da entrada, garantindo que o sistema só avance após o fornecimento de um caminho de imagem válido, evitando descrições incompletas ou genéricas.

* ## 🎬 Demonstração em Ação

Veja o sistema em funcionamento:

Solicitação do Caminho da Imagem

![image](https://github.com/user-attachments/assets/789ff2a8-8082-4251-9893-503309949c78)

Após inserir o caminho da imagem, o sistema confirma o carregamento e solicita dados adicionais não obrigatórios:

![image](https://github.com/user-attachments/assets/0be4f77b-4963-4fcc-9294-00af2def8e0a)


Em seguida, você terá a **liberdade de fornecer informações textuais adicionais** sobre o produto. Se desejar complementar a análise da imagem com detalhes como material específico, dimensões, público-alvo ou qualquer outra informação relevante, sinta-se à vontade para digitá-las. **Caso não haja informações adicionais, basta deixar o campo em branco e pressionar Enter.**

![image](https://github.com/user-attachments/assets/4aeea23c-fb1b-4430-a3f9-82693af9887f)

Para ilustrar o funcionamento do sistema, a imagem utilizada como entrada neste exemplo é mostrada abaixo. Em seguida, você poderá visualizar os resultados da descrição gerada pelos agentes:

![image](https://github.com/user-attachments/assets/2f0a34bc-c20a-4538-831a-230c189d7db1)


Abaixo, um exemplo da saída do Agente 1 (Análise da Imagem):

![image](https://github.com/user-attachments/assets/0a975d95-aec4-49e5-b734-3a02821b02cf)


Abaixo, um exemplo da saída do Agente 2 (Analista de Texto e Enriquecimento):

![image](https://github.com/user-attachments/assets/aadd107e-4594-4bfd-82d6-3f4e9019f8c7)

Abaixo, um exemplo da saída do Agente 3 (Otimizador de SEO e Redator de Descrições):

![image](https://github.com/user-attachments/assets/41b84b3b-8de5-43d7-a3a0-24b1f9f0bf2f)


## 🛠️ Como Dar Vida ao Seu Catálogo Inteligente

1.  **Abra no Google Colab:** Clique no badge [![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1QnBrHB6y1PXzuUjtzIRS7HUFsYJBxWJs?usp=sharing) para executar o código diretamente no seu navegador.
2.  **Configure sua API Key:** Certifique-se de ter configurado sua `GOOGLE_API_KEY` seguindo as instruções no notebook Colab.
3.  **Informe o Caminho da Imagem:** Quando solicitado, digite o caminho do arquivo da imagem do produto que você deseja descrever. Lembre-se, uma imagem é o ponto de partida para uma descrição poderosa!
4.  **Adicione Detalhes Exclusivos:** Compartilhe quaisquer informações textuais adicionais sobre o produto para enriquecer ainda mais a descrição gerada pela IA.
5.  **Veja a Mágica Acontecer:** Observe como os agentes trabalham em sinergia para criar uma descrição otimizada e pronta para conquistar seus clientes!

## ⚙️ Requisitos Essenciais

* **Python 3.x**
* **Bibliotecas Python:**
    * `google-generativeai`
    * `google-adk`

(Essas bibliotecas são instaladas automaticamente no notebook Colab)

## 📂 Estrutura do Código (Visão Geral)

O projeto é estruturado em um único notebook Colab, contendo as seguintes seções principais:

* **Configuração:** Importação de bibliotecas e configuração da API Gemini.
* **Função `call_agent`:** Função utilitária para interagir com os agentes Gemini.
* **Função `to_markdown`:** Função para exibir texto formatado.
* **Obtenção da Imagem:** Lógica para solicitar e carregar a imagem do produto.
* **Obtenção de Informações Textuais:** Solicitação de detalhes adicionais ao usuário.
* **Agente 1 (`agente_imagem`):** Agente responsável pela análise visual da imagem.
* **Agente 2 (`agente_analista_texto`):** Agente que combina a análise visual com informações textuais.
* **Agente 3 (implícito):** A otimização para SEO é integrada na instrução do `agente_analista_texto`.
* **Lógica Principal:** Orquestração do fluxo dos agentes.

## 🚀 Próximos Passos e Melhorias Potenciais

* Implementar um agente dedicado para a otimização de SEO com foco em palavras-chave específicas.
* Adicionar suporte para diferentes formatos de imagem.
* Integrar feedback do usuário para refinar as descrições geradas.
* Explorar a possibilidade de gerar títulos e tags para produtos.
* Criar uma interface de usuário mais interativa.

## 🤝 Contribuição

Sinta-se à vontade para explorar o código e sugerir melhorias! Se você tiver ideias para aprimorar o sistema, abra uma issue ou envie um pull request.

## 📜 Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).

## 🙏 Agradecimentos

Agradecemos à equipe do Google pela disponibilização da API Gemini e do ADK de agentes, que tornaram este projeto possível.
Um agradecimento **imensamente especial** à [Alura](https://www.alura.com.br/) pela **imersão excepcional** proporcionada ao longo desta semana em maio de 2025. O conteúdo **robusto e incrivelmente bem explicado** foi fundamental para o desenvolvimento deste projeto, e o **suporte dedicado e atencioso** na resolução de dúvidas através da comunidade no Discord fez toda a diferença na jornada de aprendizado. Muito obrigado por serem a base sólida deste trabalho!

