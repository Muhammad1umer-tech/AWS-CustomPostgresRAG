CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE qa_pairs (
    questions TEXT NOT NULL,        
    answers TEXT NOT NULL,          
    embeddings VECTOR(1534)-- The embedding column, assuming each embedding is a 300-dimensional vector
);

