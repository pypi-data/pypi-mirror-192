from sqlalchemy import select

from housenomics.transaction import Transaction
from toolbox.views import View


class ViewTransactions(View):
    def __init__(self, session, lookup, since=None, on=None) -> None:
        self._lookup = lookup
        self._session = session
        self._since = since
        self._on = on

    @property
    def data(self):
        """
        The data resulting from the view execution.
        """

        # Fetch the transactions from the database
        # TODO: use the database to filter by the lookup term
        statement = select(Transaction)
        if self._since:
            statement = statement.where(Transaction.date_of_movement >= self._since)
        if self._on:
            statement = statement.where(Transaction.date_of_movement == self._on)
        transactions = self._session.scalars(statement)

        clean_movements = []
        for t in transactions:
            clean_movements.append(
                {
                    "description": t.description,
                    "value": t.value,
                }
            )

        total: float = 0
        for movement in clean_movements:
            if self._lookup.lower() in str(movement["description"]).lower():
                total += float(movement["value"])  # type: ignore

        return total
