import os
import logging
import random
import json
from typing import List, Dict

logger = logging.getLogger(__name__)

# Cache for claims data - load once when module is imported
_claims_cache = None

def _load_claims_cache():
    """Load claims from JSON file into memory cache."""
    global _claims_cache
    if _claims_cache is not None:
        return _claims_cache
    
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dashboard_claims.json"))
    logger.info(f"[DashboardLoader] Loading claims from JSON: {json_path}")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            _claims_cache = json.load(f)
        logger.info(f"[DashboardLoader] Loaded {len(_claims_cache)} claims into cache")
        return _claims_cache
    except FileNotFoundError:
        logger.error(f"[DashboardLoader] JSON file not found: {json_path}")
        logger.error("[DashboardLoader] Please run: python scripts/convert_csv_to_json.py")
        raise
    except Exception as e:
        logger.error(f"[DashboardLoader] Error loading JSON: {str(e)}")
        raise

def load_random_dashboard_claims(n: int = 15) -> List[Dict[str, str]]:
    """
    Load random claims from the JSON cache.
    
    This is MUCH faster than loading from CSV on every request.
    The JSON file is loaded once and cached in memory.
    
    Args:
        n: Number of random claims to return (default 15)
    
    Returns:
        List of claim dictionaries with 'claim' and 'label' keys
    """
    try:
        # Load claims from cache
        all_claims = _load_claims_cache()
        
        if n <= 0:
            logger.info("[DashboardLoader] Requested sample size <= 0, returning empty list")
            return []
        
        # Generate random seed to ensure different samples each time
        random_seed = random.randint(0, 2**32 - 1)
        
        # Sample random claims
        sample_size = min(n, len(all_claims))
        random.seed(random_seed)
        sampled_claims = random.sample(all_claims, sample_size)
        
        logger.info(f"[DashboardLoader] Sampled {sample_size} claims (seed: {random_seed})")
        
        # Debug: log first 3 claims to verify randomization
        if len(sampled_claims) >= 3:
            logger.info(f"[DashboardLoader] First 3 claims: {sampled_claims[0]['claim'][:50]}..., {sampled_claims[1]['claim'][:50]}..., {sampled_claims[2]['claim'][:50]}...")
        
        return sampled_claims
        
    except Exception as e:
        logger.error(f"[DashboardLoader] Error loading claims: {str(e)}")
        raise