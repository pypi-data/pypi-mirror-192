import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from sqlalchemy import delete
from sqlalchemy.orm import Session

from housenomics.application.import_transactions import ServiceImportTransactions
from housenomics.application.list_transactions import ServiceListTransactions
from housenomics.application.views.transactions import ViewTransactions
from housenomics.infrastructure.cgd_csv_file import GatewayCGD
from housenomics.infrastructure.transactions import Transactions
from housenomics.transaction import Transaction
from toolbox.cli import CLIApplication
from toolbox.database import Database

logging_format: dict = {
    "level": logging.CRITICAL,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

logging.basicConfig(**logging_format)
logger = logging.getLogger(__name__)


class HousenomicsCLI(CLIApplication):
    help = "Housenomics helps you manage your personal finances."


housenomics_cli = HousenomicsCLI()
app = housenomics_cli.app


def import_file(file_path: Path):
    with Session(Database().engine) as session:
        gateway_cgd = GatewayCGD(file_path)
        transactions = Transactions(session)
        ServiceImportTransactions().execute(gateway_cgd, transactions)
        session.commit()


@app.command(name="import", help="Imports the transactions to feed the application")
def import_(file_path: Path):
    import_file(file_path)


def list_transactions():
    with Session(Database().engine) as session:
        results = ServiceListTransactions().execute(session)
        for m in results:
            print(f"Description: '{m.description:>22}', Value: {m.value:>10}")


@app.command(name="list", help="Lists all transactions")
def list_():
    list_transactions()


def report(seller, since, on):
    with Session(Database().engine) as session:
        view = ViewTransactions(session, seller, since, on)

    print(f"Lookup: '{seller}', Value: {round(view.data, 2)}")


@app.command(name="report", help="Builds reports according to filters")
def report_(
    seller: str,
    since: Optional[datetime] = typer.Option(
        default=None, help="Show report since specified date"
    ),
    on: Optional[datetime] = typer.Option(
        default=None, help="Show report on specified date"
    ),
):
    report(seller, since, on)


def reset():
    delete_information = typer.confirm(
        "Are you sure you want to delete all financial information ?"
    )
    if not delete_information:
        raise typer.Abort()

    db = Database()
    with Session(db.engine) as session:
        statement = delete(Transaction)
        session.execute(statement)
        session.commit()

    db.remove()


@app.command(
    name="reset",
    help="Deletes all financial information from the application",
)
def reset_():
    reset()
