from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class CompanyCreate(BaseModel):
    name : str
    nit : int
    description : Optional[str] = None
    img : Optional[str] = None
    active : bool


class CompanyUpdate(BaseModel):
    name : Optional[str] = None
    nit : Optional[int] = None
    description : Optional[str] = None
    active : Optional[bool] = None
    
    
class HeadquarterCreate(BaseModel):
    name : str
    description : Optional[str] = None
    address : str
    active : bool
    
    
class HeadquarterUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    address : Optional[str] = None
    active : Optional[bool] = None


class ContactCreate(BaseModel):
    id_headquarter : int
    number : int
    message : Optional[str] = None


class ContactUpdate(BaseModel):
    number : Optional[int] = None
    message : Optional[str] = None
    
    
class ViewCreate(BaseModel):
    name : str


class ViewUpdate(BaseModel):
    name : Optional[str] = None


class TypeCreate(BaseModel):
    id_headquarter : int
    id_view : int
    name : str
    url : str


class TypeUpdate(BaseModel):
    id_view : Optional[int] = None
    name : Optional[str] = None
    url : Optional[str] = None


class ProductCreate(BaseModel):
    id_company: int
    name : str
    description : str
    id_type : int
    recommended : str
    img : Optional[UploadFile] = None,
    price : int
    stock: int
    status: bool


class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    id_type : Optional[int] = None
    price : Optional[int] = None
    stock: Optional[int] = None
    status: Optional[bool] = None


class PermissionCreate(BaseModel):
    name : str
    description : str


class PermissionUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None


class ProfileCreate(BaseModel):
    name : str
    description : Optional[str] = None


class ProfileUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None


class ProfilePermissionManagment(BaseModel):
    id_profile: int
    id_permission: int


class UserCreate(BaseModel):
    name : str
    username : str
    email : str
    active : bool
    id_profile : int
    id_headquarter : int


class UserUpdate(BaseModel):
    name : Optional[str] = None
    username : Optional[str] = None
    email : Optional[str] = None
    active : Optional[bool] = None
    id_profile : Optional[int] = None
    id_headquarter : Optional[int] = None


class EmailData(BaseModel):
    to: str
    subject: str
    body: str