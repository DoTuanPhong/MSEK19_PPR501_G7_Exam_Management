from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.docx_parser import parse_docx
from app.core.auth import get_current_user
from app.models import User

