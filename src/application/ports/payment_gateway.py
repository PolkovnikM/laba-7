from abc import ABC, abstractmethod
from src.domain.money import Money


class PaymentGateway(ABC):
    """Интерфейс для платежного шлюза"""

    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> str:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: Money) -> None:
        pass