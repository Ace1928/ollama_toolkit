#!/usr/bin/env python3
"""
Embedding utilities for Ollama Forge.

This module provides functions for working with vector embeddings,
including similarity calculations, normalization, and batch processing.
Following Eidosian principles of exhaustive but concise implementation.
"""

from typing import Dict, List, Tuple, Any, Optional, Union
import logging
import math

# Try to import numpy for vector operations
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

logger = logging.getLogger(__name__)


def calculate_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors with elegant fallbacks.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity (between -1 and 1)
        
    Raises:
        ValueError: If vectors are empty or have different dimensions
    """
    if not vec1 or not vec2:
        raise ValueError("Vectors cannot be empty")
    
    if len(vec1) != len(vec2):
        raise ValueError(f"Vector dimensions don't match: {len(vec1)} vs {len(vec2)}")
    
    # Choose the most efficient implementation based on available libraries
    if NUMPY_AVAILABLE:
        # NumPy implementation - fastest for large vectors
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        # Handle zero vectors gracefully
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return np.dot(v1, v2) / (norm1 * norm2)
        
    else:
        # Pure Python implementation - works without dependencies
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        # Handle zero vectors gracefully
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: Input vector
        
    Returns:
        Normalized vector
        
    Raises:
        ValueError: If vector is empty or all zeros
    """
    if not vector:
        raise ValueError("Vector cannot be empty")
    
    if NUMPY_AVAILABLE:
        # NumPy implementation
        v = np.array(vector)
        norm = np.linalg.norm(v)
        
        # Handle zero vector gracefully
        if norm == 0:
            logger.warning("Cannot normalize zero vector, returning original")
            return vector
            
        return (v / norm).tolist()
    else:
        # Pure Python implementation
        norm = math.sqrt(sum(x * x for x in vector))
        
        # Handle zero vector gracefully
        if norm == 0:
            logger.warning("Cannot normalize zero vector, returning original")
            return vector
            
        return [x / norm for x in vector]


def batch_calculate_similarities(
    query_vector: List[float], 
    comparison_vectors: List[List[float]]
) -> List[Tuple[int, float]]:
    """
    Calculate similarities between a query vector and multiple comparison vectors.
    
    Args:
        query_vector: Query vector
        comparison_vectors: List of vectors to compare against
        
    Returns:
        List of (index, similarity) tuples, sorted by similarity
    """
    if not comparison_vectors:
        return []
    
    similarities = []
    for i, vec in enumerate(comparison_vectors):
        try:
            sim = calculate_similarity(query_vector, vec)
            similarities.append((i, sim))
        except ValueError as e:
            logger.warning(f"Skipping vector {i}: {e}")
            similarities.append((i, 0.0))
    
    return similarities


def process_embeddings_response(response: Dict[str, Any]) -> Optional[List[float]]:
    """
    Process the response from an embedding API call to extract the embedding vector.
    Handles different response formats from various API versions.
    
    Args:
        response: API response containing embeddings
        
    Returns:
        Extracted embedding vector or None if extraction fails
    """
    if not response:
        logger.error("Empty response received")
        return None
    
    # Handle various response formats
    if "embedding" in response:
        return response["embedding"]
    elif "embeddings" in response:
        embeddings = response["embeddings"]
        if isinstance(embeddings, list):
            # Multiple embeddings - take the first one
            if embeddings and isinstance(embeddings[0], list):
                return embeddings[0]
            # Single embedding already in list form
            return embeddings
        # Direct object containing the embedding
        return embeddings
    
    logger.error(f"Could not extract embedding from response: {list(response.keys())}")
    return None


def create_embedding_matrix(
    embeddings: List[List[float]], 
    normalize: bool = True
) -> Union[List[List[float]], Any]:
    """
    Convert a list of embeddings into a matrix for efficient operations.
    
    Args:
        embeddings: List of embedding vectors
        normalize: Whether to normalize the vectors
        
    Returns:
        Matrix of embeddings (numpy array if available, else nested list)
    """
    if not embeddings:
        return []
    
    if normalize:
        normalized = [normalize_vector(vec) for vec in embeddings]
    else:
        normalized = embeddings
    
    if NUMPY_AVAILABLE:
        return np.array(normalized)
    else:
        return normalized


def top_k_similarities(
    query_embedding: List[float],
    embedding_matrix: Union[List[List[float]], Any],
    k: int = 5
) -> List[Tuple[int, float]]:
    """
    Find top k most similar vectors to a query embedding.
    
    Args:
        query_embedding: Query vector to compare against
        embedding_matrix: Matrix of vectors to search
        k: Number of top matches to return
        
    Returns:
        List of (index, similarity) tuples for top k matches
    """
    if NUMPY_AVAILABLE and isinstance(embedding_matrix, np.ndarray):
        # Efficient numpy implementation
        query_norm = np.array(query_embedding)
        query_norm = query_norm / np.linalg.norm(query_norm)
        
        # Calculate dot products in one operation
        similarities = np.dot(embedding_matrix, query_norm)
        
        # Get top k indices
        top_indices = np.argsort(-similarities)[:k]
        return [(int(i), float(similarities[i])) for i in top_indices]
    else:
        # Fallback to pure Python implementation
        all_similarities = batch_calculate_similarities(query_embedding, embedding_matrix)
        sorted_similarities = sorted(all_similarities, key=lambda x: x[1], reverse=True)
        return sorted_similarities[:k]
