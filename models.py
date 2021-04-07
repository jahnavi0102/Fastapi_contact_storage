from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# import many
from db import Base


class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True, index=True)
   hashed_password = Column(String)
   is_active = Column(Boolean, default=True)

   contacts = relationship("Contact", back_populates="owner")


class Contact(Base):
   __tablename__ = "contacts"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, index=True)
   email = Column(String, index=True)
   phone = Column(String, index=True)
   owner_id = Column(Integer, ForeignKey("users.id"))

   owner = relationship("User", back_populates="contacts")