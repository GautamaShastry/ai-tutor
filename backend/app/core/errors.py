from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict] = None


# Error codes and messages
ERROR_CODES = {
    "AUTH_001": "Invalid credentials",
    "AUTH_002": "Session expired",
    "AUTH_003": "Unauthorized access",
    "PROFILE_001": "Profile not found",
    "PROFILE_002": "Invalid profile data",
    "PLACEMENT_001": "Placement test expired",
    "PLACEMENT_002": "Test already completed",
    "LESSON_001": "No lesson plan available",
    "CHAT_001": "Chat session not found",
    "CHAT_002": "LLM service unavailable",
    "CHAT_003": "Invalid message content",
    "REVIEW_001": "No items due for review",
    "REVIEW_002": "Item not found",
    "SKILL_001": "Concept not found",
    "SKILL_002": "Prerequisites not met",
    "RAG_001": "Vector search failed",
    "RAG_002": "Embedding generation failed",
    "DB_001": "Database connection failed",
    "DB_002": "Transaction failed",
}


class AppException(HTTPException):
    def __init__(self, error_code: str, details: Optional[dict] = None):
        message = ERROR_CODES.get(error_code, "Unknown error")
        super().__init__(
            status_code=self._get_status_code(error_code),
            detail=ErrorResponse(
                error_code=error_code,
                message=message,
                details=details,
            ).model_dump(),
        )

    def _get_status_code(self, error_code: str) -> int:
        if error_code.startswith("AUTH"):
            return 401
        if error_code.endswith("001") and "not found" in ERROR_CODES.get(error_code, "").lower():
            return 404
        return 400
