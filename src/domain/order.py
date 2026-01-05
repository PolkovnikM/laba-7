from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
import uuid
from .money import Money
from .order_status import OrderStatus
from .order_line import OrderLine


@dataclass
class Order:
    """Сущность заказа"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str = ""
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.customer_id:
            raise ValueError("ID клиента обязателен")

    @property
    def total_amount(self) -> Money:
        if not self.lines:
            return Money.zero()
        total = Money.zero()
        for line in self.lines:
            total = total + line.total()
        return total

    def add_line(self, product_id: str, product_name: str, quantity: int, price: Money) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Нельзя изменять оплаченный заказ")

        for i, line in enumerate(self.lines):
            if line.product_id == product_id:
                self.lines[i] = line.with_quantity(line.quantity + quantity)
                return

        new_line = OrderLine(
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price
        )
        self.lines.append(new_line)

    def remove_line(self, product_id: str) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Нельзя изменять оплаченный заказ")
        self.lines = [line for line in self.lines if line.product_id != product_id]

    def update_quantity(self, product_id: str, new_quantity: int) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Нельзя изменять оплаченный заказ")
        for i, line in enumerate(self.lines):
            if line.product_id == product_id:
                self.lines[i] = line.with_quantity(new_quantity)
                return
        raise ValueError(f"Товар {product_id} не найден")

    def pay(self) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Заказ уже оплачен")
        if self.status == OrderStatus.CANCELLED:
            raise ValueError("Нельзя оплатить отмененный заказ")
        if not self.lines:
            raise ValueError("Нельзя оплатить пустой заказ")
        if not self.total_amount.is_positive():
            raise ValueError("Сумма заказа должна быть положительной")

        self.status = OrderStatus.PAID
        self.paid_at = datetime.now()

    def cancel(self) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Нельзя отменить оплаченный заказ")
        self.status = OrderStatus.CANCELLED

    def is_empty(self) -> bool:
        return len(self.lines) == 0

    def is_paid(self) -> bool:
        return self.status == OrderStatus.PAID