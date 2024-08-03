from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, User
from app.services.auth_service import AuthService
from app.core.auth import create_access_token

router = APIRouter()

