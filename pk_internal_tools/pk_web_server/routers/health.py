from fastapi import APIRouter, HTTPException, status
import logging
import traceback

# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# Initialize logging for the router
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", response_model=dict, summary="Health Check", tags=["Health"])
async def health_check():
    """
    Performs a health check on the API.
    Returns:
        dict: A dictionary with a status message and current timestamp.
    Raises:
        HTTPException: If any part of the health check fails.
    """
    try:
        # Simulate a database connection check or other service checks
        # For now, just return a success status
        current_status = {"status": "ok", "timestamp": "2025-12-09T15:30:00Z"} # pk_option: Replace with actual timestamp and dynamic checks
        logger.info(f"Health check performed: {current_status['status']}")
        return current_status
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {e}"
        )
