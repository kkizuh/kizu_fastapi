from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship
from database import Base

# Пользователь
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)

# Категории транзакций
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)

# Связь "Многие ко многим" для транзакций и категорий
transaction_categories = Table(
    "transaction_categories", Base.metadata,
    Column("transaction_id", Integer, ForeignKey("transactions.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

# Транзакция
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Float)
    type = Column(String)
    date     = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    categories = relationship("Category", secondary=transaction_categories, backref="transactions")
