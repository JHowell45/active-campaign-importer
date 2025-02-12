from pydantic import BaseModel, EmailStr, Field, computed_field


class Owner(BaseModel):
    type: str
    id: int


class Contact(BaseModel):
    id: int
    email: EmailStr
    email_domain: str
    first_name: str = Field(alias="firstName", repr=False)
    last_name: str = Field(alias="lastName", repr=False)
    organization: str | None
    orgid: int
    orgname: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
