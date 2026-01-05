from dataclasses import dataclass
from decimal import Decimal
from .money import Money


@dataclass(frozen=True)
class OrderLine:
    """Строка заказа"""
    product_id: str
    product_name: str
    quantity: int
    price: Money

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if not self.product_id:
            raise ValueError("ID товара обязателен")

    def total(self) -> Money:
        return self.price * Decimal(str(self.quantity))

    def with_quantity(self, new_quantity: int) -> "OrderLine":
        if new_quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        return OrderLine(
            product_id=self.product_id,
            product_name=self.product_name,
            quantity=new_quantity,
            price=self.price
        )