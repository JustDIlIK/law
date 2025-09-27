from app.db.models import PaymentForm
from app.db.repository.base import BaseRepository


class PaymentFormRepository(BaseRepository):
    model = PaymentForm
