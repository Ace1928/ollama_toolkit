#!/usr/bin/env python3
"""
Utilities for working with embeddings in the Ollama Toolkit.

This module provides functions for comparing and analyzing vector embeddings,
including cosine similarity calculation, normalization, and vector operations.
"""

import math
import logging
from typing import List, Optional, Tuple, Union, Dict, Any

import numpy as np

logger = logging.getLogger(__name__)

def calculate_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two embedding vectors.
    
    Args:
        vec1: First embedding vector
        vec2: Second embedding vector
        
    Returns:
        Cosine similarity score between -1 and 1
        
    Raises:
        ValueError: If vectors are empty or have different dimensions
    """
    if not vec1 or not vec2:
        raise ValueError("Vectors cannot be empty")
    
    if len(vec1) != len(vec2):
        raise ValueError(f"Vectors must have same dimensions: {len(vec1)} != {len(vec2)}")
    
    # Calculate cosine similarity: dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    
    # Handle zero vectors
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: Input vector
        
    Returns:
        Normalized vector with magnitude 1
    """
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude > 0:
        return [x / magnitude for x in vector]
    return [0.0] * len(vector)

def batch_calculate_similarities(
    query_vector: List[float], 
    comparison_vectors: List[List[float]]
) -> List[Tuple[int, float]]:
    """
    Calculate similarities between query vector and multiple comparison vectors.
    
    Args:
        query_vector: Reference vector to compare against
        comparison_vectors: List of vectors to compare with the query
        
    Returns:
        List of (index, similarity) tuples sorted by descending similarity
    """
    if not query_vector or not comparison_vectors:
        return []
    
    results = []
    for i, vec in enumerate(comparison_vectors):
        try:
            similarity = calculate_similarity(query_vector, vec)
            results.append((i, similarity))
        except ValueError as e:
            logger.warning(f"Skipping vector at index {i}: {e}")
    
    # Sort by similarity score (descending)
    return sorted(results, key=lambda x: x[1], reverse=True)

def process_embeddings_response(
    response: Dict[str, Any]
) -> Optional[List[float]]:
    """
    Extract embedding from API response.
    
    Args:
        response: API response from embedding endpoint
        
    Returns:
        List of embedding values or None if not found
    """
    if not response:
        return None
    
    if "embedding" in response:
        return response["embedding"]
    
    # Some models use 'embeddings' key instead
    if "embeddings" in response:
        embeddings = response["embeddings"]
        if isinstance(embeddings, list) and embeddings:
            # First embedding if it's a list of embeddings
            if isinstance(embeddings[0], list):
                return embeddings[0]
            return embeddings
    
    logger.warning(f"No embedding found in response: {list(response.keys())}")
    return None
