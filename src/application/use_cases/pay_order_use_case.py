from typing import Dict, Any
from src.application.ports.order_repository import OrderRepository
from src.application.ports.payment_gateway import PaymentGateway


class PayOrderUseCase:
    """Use Case для оплаты заказа"""

    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, order_id: str) -> Dict[str, Any]:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Заказ {order_id} не найден")

        order.pay()

        transaction_id = self.payment_gateway.charge(
            order_id=order_id,
            amount=order.total_amount
        )

        self.order_repository.save(order)

        return {
            "success": True,
            "order_id": order_id,
            "transaction_id": transaction_id,
            "amount": str(order.total_amount),
            "status": order.status.value
        }