"""Helpers du module user_manager."""
# helper.py
from typing import Any, Type

import bcrypt
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# fonction permettant de verifier si un objet existe pour une certaine classe
async def verify_bd_object (db: AsyncSession , class_model: Type[Any] ,class_attr: str, identifier: UUID4):
    
    try:
        attribute = getattr(class_model , class_attr)
    except AttributeError as exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"an error ocured. Exception : {str(exception)}"
        )
    
    query_stmt = await db.execute(select(class_model).where(
        and_(class_model.attribute == identifier , class_model.deleted_at.is_(None))
    ))
    
    query_result = query_stmt.scalar_one_or_none()
    if len(query_result) > 0:
        return True

    return False