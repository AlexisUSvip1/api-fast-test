from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate


class AuthService:

    @staticmethod
    async def register(
        db: AsyncSession,
        user_data: UserCreate
    ):

        existing_user = await UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise ValueError(
                "Email already exists"
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(
                user_data.password
            ),
        )

        return await UserRepository.create(
            db,
            user,
        )

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str,
    ):

        user = await UserRepository.get_by_email(
            db,
            email,
        )

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        if not verify_password(
            password,
            user.password,
        ):
            raise ValueError(
                "Invalid credentials"
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }