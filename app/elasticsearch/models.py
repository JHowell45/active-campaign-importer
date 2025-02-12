from elasticsearch_dsl import Document, InnerDoc

from app.importer.models.tasks import Task


class Note(Document): ...


class Contact(Document): ...


class Owner(InnerDoc):
    type: str
    id: int


class Links(InnerDoc):
    activities: str
    automation: str
    dealTasktype: str
    doneAutomation: str
    notes: str
    owner: str
    taskNotifications: str
    user: str
    assignee: str


class Task(Document):
    id: int
    status: int
    title: str
    note: str
    user_id: int
    assignee_id: int
    links: Links
    owner: Owner
    due_date: datetime
    edate: datetime
    cdate: datetime
    udate: datetime
    outcome_id: int
    outcome_info: str

    class Index:
        name = "tasks"

    def from_api(cls, task: Task) -> "Task":
        pass
