from datetime import datetime

import requests
from pydantic import BaseModel, EmailStr, computed_field

from app.importer.api.core import get_headers
from app.importer.models.contacts import Contact, Owner


class Note(BaseModel):
    id: int
    is_draft: bool
    links: dict[str, str]
    mdate: datetime
    note: str
    owner: Owner
    relid: int
    reltype: str

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def contact(self) -> Contact | None:
        response = requests.get(self.links["owner"], headers=get_headers())
        data = response.json()
        if data and "contact" in data:
            contact = Contact(**data["contact"])
            return contact
        return None

    def row_data(self) -> tuple[str | None, EmailStr | None, str | None, str]:
        contact_name: str | None = None
        contact_email: EmailStr | None = None
        organization: str | None = None

        if self.contact:
            contact_name = self.contact.name
            contact_email = self.contact.email

        return (contact_name, contact_email, organization, self.note)
