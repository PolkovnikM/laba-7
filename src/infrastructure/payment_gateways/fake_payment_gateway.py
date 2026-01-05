import uuid
from typing import Dict
from src.domain.money import Money
from src.application.ports.payment_gateway import PaymentGateway


class FakePaymentGateway(PaymentGateway):

    def __init__(self):
        self.transactions: Dict[str, Dict] = {}
        self.should_fail = False

    def charge(self, order_id: str, amount: Money) -> str:
        if self.should_fail:
            raise ValueError("Платежный шлюз недоступен")

        if amount.is_zero() or not amount.is_positive():
            raise ValueError("Сумма платежа должна быть положительной")

        transaction_id = str(uuid.uuid4())
        self.transactions[transaction_id] = {
            "order_id": order_id,
            "amount": amount,
            "status": "completed"
        }

        return transaction_id

    def refund(self, transaction_id: str, amount: Money) -> None:
        if transaction_id not in self.transactions:
            raise ValueError(f"Транзакция {transaction_id} не найдена")

        transaction = self.transactions[transaction_id]
        transaction["status"] = "refunded"
        transaction["refund_amount"] = amount

    def set_fail_mode(self, should_fail: bool) -> None:
        self.should_fail = should_fail