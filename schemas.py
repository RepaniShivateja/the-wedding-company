from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationCreate(BaseModel):
    organization_name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)


class OrganizationUpdate(BaseModel):
    organization_name: str = Field(..., min_length=2)
    new_organization_name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=6)


class OrganizationResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_email: EmailStr
    connection_info: dict


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GenericMessage(BaseModel):
    message: str

