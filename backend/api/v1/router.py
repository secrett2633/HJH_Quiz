from fastapi import APIRouter

from backend.api.v1 import auth, users, quiz

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
