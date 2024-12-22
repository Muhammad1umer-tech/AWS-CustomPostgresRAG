from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import psycopg2
import os

load_dotenv()
client = OpenAI()

def get_embedding(text):
    model="text-embedding-3-small"
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding


def document_to_response(input, content):
    system_prompt = ("""
        You are an AI assistant that convert the content into readable 4,5 lines paragraph according to user input.
        paragraph should be according to user input and use content to make the paragraph.
        
        IMPORTANT: make content in a readable format according to user input into readable 4,5 lines paragraph.
        input: {input},
        content: {content} """)
    
    prompt = ChatPromptTemplate([
        ("system", system_prompt)
    ])
    
    chain = prompt | ChatOpenAI() | StrOutputParser()
    response = chain.invoke({"input": input, "content": content})
    return response


def check_file():
    file_path = os.getenv("CSV_FILE_PATH")
    df = pd.read_csv(file_path)
    print(df.heads())

def create_db():
    # Get connection details from environment variables
    db_host = os.getenv('POSTGRES_ENDPOINT')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    db_port = os.getenv('POSTGRES_PORT', 5432)
    print(db_host, db_user, db_password, db_name, db_port)
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        dbname=db_name,
        port=db_port
    )
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;"),
    cursor.execute("""
        CREATE TABLE qa_pairs (
        questions TEXT NOT NULL,        
        answers TEXT NOT NULL,          
        embeddings VECTOR(1536)--);"""),
    
     conn.commit()
        cursor.close()
        conn.close()

# Use the connection to interact with the database


def create_db():
    try:    
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DB")
        postgres_endpoint = os.getenv("POSTGRESS_ENDPOINT")
        postgres_port = os.getenv("POSTGRESS_PORT")
        # Connect to PostgreSQL
        # Database connection
        conn = psycopg2.connect(
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password,
            host=postgres_endpoint,
            port=postgres_port)
        
        cursor = conn.cursor()

        # Read data from CSV using pandas
        file_path = os.getenv("CSV_FILE_PATH")
        df = pd.read_csv(file_path)

        # Insert data into the database along with embeddings
        for index, row in df.iterrows():
            question = row['questions']
            answer = row['answers']    
            # Get the embedding for the question
            embedding = get_embedding(question)  # Fetch embedding from OpenAI
            
            
            # Insert data into the qa_pairs table
            cursor.execute(
                "INSERT INTO qa_pairs (questions, answers, embeddings) VALUES (%s, %s, %s)",
                (question, answer, embedding)
            )

        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error while Data insertion, {e}")


def input_to_response(input):    
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")
    postgres_endpoint = os.getenv("POSTGRESS_ENDPOINT")
    postgres_port = os.getenv("POSTGRESS_PORT")
    # Connect to PostgreSQL
    # Database connection
    conn = psycopg2.connect(
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        host=postgres_endpoint,
        port=postgres_port)

    cursor = conn.cursor()
    
    # get embeddings to user input
    query_vector = get_embedding(input)
    
    # Ensure the query vector is passed as a string formatted for PostgreSQL's vector type
    query_vector_str = f"ARRAY[{','.join(map(str, query_vector))}]"

    # Update the query to use explicit casting to vector
    cursor.execute(f"""
        SELECT questions, answers, 
            1 - (embeddings <=> {query_vector_str}::vector) AS similarity
        FROM qa_pairs
        ORDER BY similarity DESC
        LIMIT 5;
    """)


    # Fetch and display the results
    results = cursor.fetchall()
    
    # for result in results:
    #     print(f"Question: {result[0]}")
    #     print(f"Answer: {result[1]}")
    #     print(f"Similarity: {result[2]}")
    #     print('-' * 80)
    
    # Combine all questions and answers into a single string without using a loop
    combined_retrieved_q_a = '\n'.join(
        [f"Question: {result[0]}, Answer: {result[1]}" for result in results]
    )
    response = document_to_response(input, combined_retrieved_q_a)
    
    cursor.close()
    conn.close()
    
    return response



create_db()    
input_to_response("have you experience with php and laravel?")

