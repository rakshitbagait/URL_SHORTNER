from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from db import Base

import secrets
import string
from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    url: HttpUrl
class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(8), unique=True, nullable=False, index=True)
    clicks = Column(Integer, default=0)

    @staticmethod
    def generate_short_code(length: int = 8):
        """
        Generate a random secure short code.
        """

        characters = string.ascii_letters + string.digits

        return "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

    @classmethod
    def shorten_url(cls, db: Session, original_url: str):
        """
        Creates a shortened URL.
        Returns the existing URL if it has already been shortened.
        """

        existing_url = (
            db.query(cls)
            .filter(cls.original_url == original_url)
            .first()
        )

        if existing_url:
            return existing_url

        short_code = cls.generate_short_code()

        while (
            db.query(cls)
            .filter(cls.short_code == short_code)
            .first()
        ):
            short_code = cls.generate_short_code()

        new_url = cls(
            original_url=original_url,
            short_code=short_code
        )

        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        return new_url

    @classmethod
    def get_by_short_code(cls, db: Session, short_code: str):
        """
        Returns the URL object using the short code.
        """

        return (
            db.query(cls)
            .filter(cls.short_code == short_code)
            .first()
        )

    def increment_clicks(self, db: Session):
        """
        Increment click count.
        """

        self.clicks += 1

        db.commit()

        db.refresh(self)