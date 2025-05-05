from sqlalchemy import Date, String, DateTime, func, Integer, Column, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from datetime import date, datetime

class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy ORM models.

    This class serves as the base for all database models in the application,
    providing a foundation for declarative database mapping using SQLAlchemy ORM.
    """
    pass

class Contact(Base):
    """Represents a contact in the database.

    This model stores contact information including personal details, contact methods,
    and metadata about contact creation and updates.

    Attributes:
        id (int): Unique identifier for the contact.
        first_name (str): First name of the contact (max 50 characters).
        last_name (str): Last name of the contact (max 50 characters).
        email (str): Email address of the contact (unique, max 100 characters).
        phone (str): Phone number of the contact (max 20 characters).
        birthday (date, optional): Birthday of the contact.
        created_at (datetime): Timestamp of contact creation.
        updated_at (datetime): Timestamp of last contact update.
        user_id (int, optional): ID of the associated user.
        user (User): Relationship to the User model.
    """
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="notes")


class User(Base):
    """Represents a user in the database.

    This model stores user authentication and profile information.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        email (str): Unique email address of the user.
        hashed_password (str): Securely hashed password for user authentication.
        created_at (datetime): Timestamp of user account creation.
        avatar (str, optional): URL or path to the user's avatar image.
        confirmed (bool): Flag indicating whether the user has confirmed their account.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)