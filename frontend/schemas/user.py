from pydantic import BaseModel, EmailStr


class __UserBase(BaseModel):
    """User base for authentication"""

    name: str
    password: str


class UserPost(__UserBase):
    """
    name: nombre del usuario.\n
    password: passsword del usuario.\n
    email: Direccion de correo electronico del usuario.\n
    """

    email: EmailStr


class UserGet(__UserBase):
    about: str


class User(__UserBase):
    """
    id: identificador del usuario.\n
    """

    id: int
