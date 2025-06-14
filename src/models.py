from sqlalchemy import (Column, Integer,
                        String, ForeignKey,
                        DateTime, UniqueConstraint)
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    borrowed_books = relationship("BorrowedBook", back_populates="reader")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    copies = Column(Integer, default=1, nullable=False)

    borrowed_books = relationship("BorrowedBook", back_populates="book")


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="borrowed_books")
    reader = relationship("Reader", back_populates="borrowed_books")

    __table_args__ = (
        UniqueConstraint("book_id", "reader_id", "return_date", name="uq_active_borrow"),
    )