from db.base_class import Base
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    blogs = relationship("Blog", back_populates="author")
