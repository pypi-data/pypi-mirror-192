from sqlalchemy import select

from housenomics.transaction import Transaction


class ServiceListTransactions:
    # TODO: this is the same as ViewTransactions
    def execute(self, session):
        statement = select(Transaction)
        return session.scalars(statement).all()
