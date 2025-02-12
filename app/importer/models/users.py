from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    username: str
    first_name: str = Field(alias="firstName", repr=False)
    last_name: str = Field(alias="lastName", repr=False)
    email: EmailStr
