from typing import Dict, Optional
from src.domain.order import Order
from src.application.ports.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self._orders: Dict[str, Order] = {}

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def delete(self, order_id: str) -> None:
        if order_id in self._orders:
            del self._orders[order_id]

    def clear(self) -> None:
        self._orders.clear()