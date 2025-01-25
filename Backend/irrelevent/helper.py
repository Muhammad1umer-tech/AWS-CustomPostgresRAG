from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings 
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector
from dotenv import load_dotenv
import os

load_dotenv()       

# See docker command above to launch a postgres instance with pgvector enabled.
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")
postgres_host = os.getenv("POSTGRES_HOST")  # the service name from Docker Compose
postgres_port = os.getenv("POSTGRES_PORT")  # the default PostgreSQL port inside the container

connection = f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
file_path = "questions.csv" 
collection_name = "docs"

vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True)

def create_database():
    try:
        loader = CSVLoader(file_path=file_path)
        datas = loader.load()
        vector_store.add_documents(datas, ids=[data.metadata["row"] for data in datas])
        print("\nsuccessfully created the database")
        return "successfully created the database"
    except Exception as e:
        print("\nError while creating Database, {e}")
        return "Error while creating Database, {e}"  

def run_query_pgvector_get_response(query):
    try:
        docs = vector_store.similarity_search(query, k=4)
        if len(docs) == 0:
            return "No relevent doc retrived, either database is not inilized."
            
        content = docs[0].page_content
        print("\n\ncontent: ", content)
        response = document_to_response(query, content)
        print("\n\nresponse: ", response)
        return response
    
    except Exception as e:
        print("\nError while run_query_pgvector, {e}")
        return "Error while run_query_pgvector, {e}"
        
        
def del_db():
    try:
        loader = CSVLoader(file_path=file_path)
        datas = loader.load()
        ids=[data.metadata["row"] for data in datas]
        vector_store.delete(ids=ids)
    
        print("\nsuccessfully deleted the database")
        return "successfully deleted the database"
    except Exception as e:
        print("\nError while deleting the database, {e}")
        return "Error while deleting the database, {e}"


def document_to_response(input, content):
    system_prompt = ("""
        You are an AI assistant that connected to a 
        vector database containing all my past projects and tasks.
        My team has access to use you When responding to client queries, the team 
        will first consult the assistant to determine if I've previously addressed 
        similar questions or worked on related projects. If relevant information exists, the assistant 
        will generate an accurate response based on the database and the input provided. 
        If no relevant information is found, the assistant should refrain from providing 
        unrelated or speculative responses and answer according to given content
        
        IMPORTANT: use content to make custom response to answr input.
        input: {input},
        content: {content} """)
    
    prompt = ChatPromptTemplate([
        ("system", system_prompt)
    ])
    
    chain = prompt | ChatOpenAI() | StrOutputParser()
    response = chain.invoke({"input": input, "content": content})
    return response



# create_database()
# print("\nnow")
# print(run_query_pgvector(vector_store, "have you worked with django middleware? "))
