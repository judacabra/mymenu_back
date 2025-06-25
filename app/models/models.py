from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import VARCHAR


Base = declarative_base()
String = VARCHAR(255)

class Company(Base):
    __tablename__ = "company"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    nit = Column(BigInteger, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)
    img = Column(String)
    active = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    contact = relationship("Contact", back_populates="company")
    user = relationship("User", back_populates="company")
    product = relationship("Product", back_populates="company")
    type = relationship("Type", back_populates="company")


class Contact(Base):
    __tablename__ = "contact"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_company = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    number = Column(BigInteger, nullable=False)
    message = Column(String)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="contact")
    
    
class View(Base):
    __tablename__ = "view"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    type = relationship("Type", back_populates="view")


class Type(Base):
    __tablename__ = "type"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_company = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    id_view = Column(BigInteger, ForeignKey("view.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    view = relationship("View", back_populates="type")
    company = relationship("Company", back_populates="type")
    product = relationship("Product", back_populates="type")


class Product(Base):
    __tablename__ = "product"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_company = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    id_type = Column(BigInteger, ForeignKey("type.id"), nullable=False)
    recommended = Column(String, default="NO", nullable=False)
    img = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    stock = Column(BigInteger, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    type = relationship("Type", back_populates="product")
    company = relationship("Company", back_populates="product")


class Permission(Base):
    __tablename__ = "permission"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    profile_permissions = relationship("ProfilePermission", back_populates="permission")


class Profile(Base):
    __tablename__ = "profile"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="profile")
    profile_permissions = relationship("ProfilePermission", back_populates="profile", cascade="all, delete")


class ProfilePermission(Base):
    __tablename__ = "profile_permission"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id_profile = Column(BigInteger, ForeignKey("profile.id"), nullable=False)
    id_permission = Column(BigInteger, ForeignKey("permission.id"), nullable=False)

    profile = relationship("Profile", back_populates="profile_permissions")
    permission = relationship("Permission", back_populates="profile_permissions")


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    id_profile = Column(BigInteger, ForeignKey("profile.id"), nullable=False)
    id_company = Column(BigInteger, ForeignKey("company.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    profile = relationship("Profile", back_populates="user")
    company = relationship("Company", back_populates="user")
