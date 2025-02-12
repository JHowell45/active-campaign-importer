from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel, Field


class Spreadsheet(BaseModel):
    name: str = Field(..., frozen=True)
    titles: list[str]
    book: Workbook | None = Field(default=None, init=False)
    sheet: Worksheet | None = Field(default=None, init=False)

    class Config:
        arbitrary_types_allowed = True

    def model_post_init(self, __context):
        self.book = Workbook()
        self.sheet = self.book.active
        self.sheet.append(self.titles)
        return super().model_post_init(__context)

    def append(self, values: list) -> None:
        if len(self.titles) != len(values):
            raise Exception("Invalid values size!!")
        self.sheet.append(values)

    def save(self) -> None:
        self.book.save(filename=f"{self.name}.xlsx")
