from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from db import SessionLocal
from models import Memory
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Load a pre-trained sentence transformer model.
# 'all-MiniLM-L6-v2' is a good balance of speed and quality, producing 384-dim embeddings.
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    model = None

def get_db_session():
    """Generator function to get a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_memory(content: str, metadata: dict = None):
    """
    Adds a new memory to the database, generating embeddings locally.
    """
    if not model:
        raise RuntimeError("SentenceTransformer model is not loaded.")
        
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        embedding = model.encode(content)
        new_memory = Memory(
            content=content,
            embedding=embedding,
            metadata=metadata
        )
        db.add(new_memory)
        db.commit()
        db.refresh(new_memory)
        logger.info(f"Added new memory with ID: {new_memory.id}")
        return new_memory
    finally:
        next(db_session_gen, None) # Ensure the session is closed

def search_memory(query: str, limit: int = 5):
    """
    Performs a semantic search on the memory database.
    """
    if not model:
        raise RuntimeError("SentenceTransformer model is not loaded.")

    db_session_gen = get_db_session()
    db = next(db_session_gen)

    try:
        query_embedding = model.encode(query)
        # Use the l2_distance operator from pgvector for similarity search
        results = db.query(Memory).order_by(Memory.embedding.l2_distance(query_embedding)).limit(limit).all()
        return results
    finally:
        next(db_session_gen, None)

def get_memory(memory_id: int):
    """
    Retrieves a specific memory by its ID.
    """
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    try:
        return db.query(Memory).filter(Memory.id == memory_id).first()
    finally:
        next(db_session_gen, None)

def get_all_memories():
    """
    Retrieves all memories.
    """
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    try:
        return db.query(Memory).all()
    finally:
        next(db_session_gen, None)
