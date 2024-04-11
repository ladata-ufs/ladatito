# Documentação - ladatito
> Os documentos utilizados no RAG estão em 📁 `textos`

## `GeminiRAG.py`

### `EnviromentLADATITO`
* `load_pdf`<br>
    recebe uma lista de documentos e itera sobre eles, extraindo os textos de cada uma das páginas lidas;

* `split_text`<br>
    chama a função `load_pdf` e divide os textos extraídos em parágrafos;

* `create_chroma_db`<br>
    cria o banco de textos, armazenando parágrafo por parágrafo;

* `load_chroma_collection`<br>
    acessa o banco de textos criado.

### `Generate LADATITO`
* `get_relevant_passage`<br>
    responsável por extrair os parágrafos relevantes dos documentos carregados, com base na query enviada pelo usuário;

* `make_rag_prompt`<br>
    Utiliza os parágrafos relevantes com um prompt personalizado para gerar um prompt direcionado a perguntas relacionadas à LADATA;

* `make_general_prompt`<br>
    Gera um prompt personalizado direcionado a perguntas gerais;

* `generate_answer`<br>
    Utiliza-se do Gemini como gerador de texto de resposta, recebendo um prompt ou pergunta como entrada;

* `respond_query`<br>
    Combina o prompt personalizado gerado pela função `make_rag_prompt` e o modelo da função `generate_answer` na geração de uma resposta relacionada à LADATA;

* `respond_general_query`<br>
    Combina o prompt personalizado gerado pela função `make_general_prompt` e o modelo da função `generate_answer` na geração de uma resposta geral;

* `exibir_resposta`<br>
    Formata e exibe a mensagem no notebook.
