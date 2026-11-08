from sqlmodel import SQLModel
from schemas.payments import Payment, PaymentFilters


class DBPayments(SQLModel):
    """Base de Pagos."""

    def get_payments(self):
        return ""

    def get_payment(self):
        return {}

    def created_payment(self):
        return {}
