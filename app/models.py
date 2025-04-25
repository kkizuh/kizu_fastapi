from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)

transaction_categories = Table(
    "transaction_categories", Base.metadata,
    Column("transaction_id", Integer, ForeignKey("transactions.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Float)
    type = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    categories = relationship("Category", secondary=transaction_categories, backref="transactions")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
