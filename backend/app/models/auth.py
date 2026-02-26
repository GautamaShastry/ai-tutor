from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: str
    password: str
    native_language: str
    target_goal: str
    daily_time_minutes: int = 15
    style_preference: str = "gentle"
    domains: list[str] = []
