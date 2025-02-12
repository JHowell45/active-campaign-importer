from tqdm import tqdm
from typer import Typer

from app.excel.builder import Spreadsheet
from app.importer.api.models import TaskResponse
from app.importer.api.query import pagination

populate_cli = Typer(
    short_help="Populates the elasticsearch indices with the relevant data."
)


@populate_cli.command()
def notes() -> None:
    xlsx: Spreadsheet = Spreadsheet(
        name="katy_tasks",
        titles=[
            "TITLE DESCRIPTION",
            "RELATED TO NAME",
            "RELATED TO EMAIL",
            "STATUS",
            "TYPE",
        ],
    )
    page: int = 0
    response: TaskResponse = pagination(
        "dealTasks", TaskResponse, page, filters={"userid": 2}, limit=3
    )
    with tqdm(total=response.meta.total) as pbar:
        while response.count > 0:
            for task in response.data:
                if task.user_id == 2:
                    xlsx.append(
                        [
                            task.title,
                            task.owner.name if task.owner else None,
                            task.owner.email if task.owner else None,
                            task.status,
                            task.task_type.title if task.task_type else None,
                        ]
                    )
                    xlsx.save()
                pbar.update(1)
            page += 1
            response = pagination(
                "dealTasks", TaskResponse, page, filters={"userid": 2}, limit=3
            )
