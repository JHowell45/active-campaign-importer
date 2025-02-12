from datetime import datetime

import requests
from pydantic import BaseModel, EmailStr, Field, HttpUrl, computed_field
from rich import print  # noqa

from app.importer.api.core import get_headers


class OwnerData(BaseModel):
    type: str
    id: int


class ActivityLinks(BaseModel):
    user_link: HttpUrl = Field(alias="user")
    recipients_link: HttpUrl = Field(alias="recipients")
    reference_link: HttpUrl = Field(alias="reference")
    notes_link: HttpUrl = Field(alias="notes")


class ActivityData(BaseModel):
    data_id: int
    data_type: str
    data_action: str
    data_oldval: str
    outcome_title: str
    outcome_info: str


class ActivityReference(BaseModel):
    id: int
    type: str


class Activity(BaseModel):
    id: int
    subscriber_id: int = Field(alias="subscriberid")
    user_id: int = Field(alias="userid")
    permission: str
    referenceModelName: str
    reference_type: str
    reference_id: int
    reference_action: str
    jsonData: str | None
    links: ActivityLinks
    reference: ActivityReference
    tstamp: datetime


class TaskLinks(BaseModel):
    activities_link: HttpUrl = Field(alias="activities", repr=False)
    automation_link: HttpUrl = Field(alias="automation", repr=False)
    deal_task_type: HttpUrl = Field(alias="dealTasktype", repr=False)
    doneAutomation_link: HttpUrl = Field(alias="doneAutomation", repr=False)
    notes_link: HttpUrl = Field(alias="notes", repr=False)
    owner_link: HttpUrl = Field(alias="owner", repr=False)
    taskNotifications_link: HttpUrl = Field(alias="taskNotifications", repr=False)
    user_link: HttpUrl = Field(alias="user", repr=False)
    assignee_link: HttpUrl = Field(alias="assignee", repr=False)

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def activities(self) -> list[Activity] | None:
        response = requests.get(self.activities_link, headers=get_headers())
        data = response.json()
        return [
            Activity.model_validate(activity, context={"link": self.activities_link})
            for activity in data["activities"]
        ]


class TaskType(BaseModel):
    id: int
    title: str
    status: int
    created: datetime | None = Field(alias="created_utc_timestamp")
    updated: datetime | None = Field(alias="updated_utc_timestamp")


class OwnerLinks(BaseModel):
    contact_data_link: HttpUrl = Field(alias="contactData")


class Owner(BaseModel):
    id: int
    first_name: str = Field(alias="firstName", repr=False)
    last_name: str = Field(alias="lastName", repr=False)
    email: EmailStr
    organisation_id: int = Field(alias="orgid")
    organisation_name: str = Field(alias="orgname")
    links: OwnerLinks

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class User(BaseModel):
    id: int
    first_name: str = Field(alias="firstName", repr=False)
    last_name: str = Field(alias="lastName", repr=False)

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Task(BaseModel):
    id: int
    status: int
    title: str
    note: str
    user_id: int = Field(alias="user")
    assignee_id: int = Field(alias="assignee")
    links: TaskLinks
    owner_data: OwnerData = Field(alias="owner", repr=False)
    due_date: datetime = Field(alias="duedate")
    edate: datetime
    cdate: datetime
    udate: datetime
    outcome_id: int | None = Field(alias="outcomeId")
    outcome_info: str | None = Field(alias="outcomeInfo")

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def owner(self) -> Owner | None:
        if self.owner_data.type != "contact":
            return None
        response = requests.get(self.links.owner_link, headers=get_headers())
        data = response.json()
        # print(data)
        return Owner(**data[self.owner_data.type])

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def user(self) -> User | None:
        response = requests.get(self.links.user_link, headers=get_headers())
        data = response.json()
        # print(data)
        return User(**data["user"])

    @computed_field(repr=True)  # type: ignore[prop-decorator]
    @property
    def task_type(self) -> TaskType | None:
        response = requests.get(self.links.deal_task_type, headers=get_headers())
        data = response.json()
        # print(data)
        return TaskType(**data["dealTasktype"])
