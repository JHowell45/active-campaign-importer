from tqdm import tqdm
from typer import Typer

from app.cli.elasticsearch import elasticsearch_cli
from app.cli.populate import populate_cli
from app.excel.builder import Spreadsheet
from app.importer.api.query import pagination

cli = Typer()
cli.add_typer(populate_cli, name="populate")
cli.add_typer(elasticsearch_cli, name="es")


@cli.command()
def create_notes_spreadsheet() -> None:
    xlsx: Spreadsheet = Spreadsheet(
        name="active_campaign_notes",
        titles=["CONTACT NAME", "CONTACT EMAIL", "ORGANIZATION", "NOTE"],
    )
    page: int = 0
    # response = pagination("notes", page)
    # with tqdm(total=response.meta.total) as pbar:
    #     while response.count > 0:
    #         page += 1
    #         for note in response.notes:
    #             xlsx.append(note.row_data())
    #             xlsx.save()
    #             pbar.update(1)
    #         response = pagination("notes", page)

    #     xlsx.save()
