from abc import ABC, abstractmethod
from typing import Optional
from src.domain.order import Order


class OrderRepository(ABC):
    """Интерфейс для работы с заказами"""

    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete(self, order_id: str) -> None:
        pass