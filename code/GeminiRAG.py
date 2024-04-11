import chromadb
from typing import List
from pypdf import PdfReader
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv

from embedding import GeminiEmbeddingFunction

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class EnviromentLADATITO():
    
    def __init__(self):
        self.key = GOOGLE_API_KEY
        self.arquivos = ["code/textos/Estatuto da Liga Acadêmica de Ciência de Dados (LADATA).pdf", "code/textos/Estatuto da Liga Acadêmica de Ciência de Dados (LADATA).pdf"]
        self.db_path = "bot_ladata/data/"
        self.name = "ladatito"

    def load_pdf(self):
        text = ""

        for arquivo in self.arquivos:
            reader = PdfReader(arquivo)

            for page in reader.pages:
                text += page.extract_text()

        return text

    def split_text(self):

        text = self.load_pdf()
        split_text = re.split('/n /n', text)
        return [i for i in split_text if i != ""]

    def create_chroma_db(self):

        chroma_client = chromadb.PersistentClient(path= self.db_path)
        db = chroma_client.create_collection(name= self.name, embedding_function=GeminiEmbeddingFunction())

        for i, d in enumerate(self.split_text()):
            db.add(documents=d, ids=str(i))

        return db, self.name
    
    def load_chroma_collection(self):
        chroma_client = chromadb.PersistentClient(path = self.db_path)
        db = chroma_client.get_collection(name = self.name, embedding_function=GeminiEmbeddingFunction())

        return db

class GenerateLADATITO(EnviromentLADATITO):
    
    def __init__(self):
        self.enviroment = EnviromentLADATITO().create_chroma_db()
        self.db = EnviromentLADATITO().load_chroma_collection()
        self.key = GOOGLE_API_KEY
    
    def get_relevant_passage(self, query):
        passage = self.db.query(query_texts=[query], n_results=100)['documents'][0]
        return passage
    

    def make_rag_prompt(self, query, relevant_passage):
        escaped = relevant_passage.replace("'", "").replace('"', "").replace("/n", " ")
        prompt = ("""Você é um bot útil e informativo, chamado Ladatito, que responde a perguntas sobre a LADATA usando o texto da passagem de referência incluída abaixo. /
        Certifique-se de responder em uma frase completa, sendo abrangente, incluindo todas as informações básicas relevantes. /
        No entanto, você está falando para um público não técnico, portanto, analise conceitos complicados e/ou
        adote um tom amigável e descontraído, de modo a sempre cumprimentar seu público de forma calorosa. Caso queiram saber quem você é, identifique-se como Ladatito e explique que sua função é tirar toda e quaisquer dúvidas em relação à LADATA. /
        Se a passagem for irrelevante para a resposta, você pode ignorá-la.
        PERGUNTA: '{query}'
        PASSAGEM: '{relevant_passage}'

        RESPOSTA:
        """).format(query=query, relevant_passage=escaped)

        return prompt


    def generate_answer(self, prompt):
        
        genai.configure(api_key= self.key)
        model = genai.GenerativeModel('gemini-pro')
        answer = model.generate_content(prompt)
        
        return answer.text

    def respond_query(self, query):
        relevant_text = self.get_relevant_passage(query)
        prompt = self.make_rag_prompt(query, relevant_passage="".join(relevant_text)) # joining the relevant chunks to create a single passage
        
        answer = self.generate_answer(prompt)

        return answer
