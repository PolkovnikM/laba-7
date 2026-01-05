import pytest
from decimal import Decimal
from src.domain.money import Money
from src.domain.order import Order
from src.application.use_cases.pay_order_use_case import PayOrderUseCase
from src.infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from src.infrastructure.payment_gateways.fake_payment_gateway import FakePaymentGateway


class TestPayOrderUseCase:

    def setup_method(self):
        self.order_repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.order_repository, self.payment_gateway)

    def test_successful_payment(self):
        order = Order(customer_id="customer_123")
        order.add_line("prod_1", "Товар 1", 2, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        result = self.use_case.execute(order.id)

        assert result["success"] is True
        assert result["order_id"] == order.id
        assert "transaction_id" in result

        saved_order = self.order_repository.get_by_id(order.id)
        assert saved_order.is_paid()
        assert saved_order.status.value == "paid"

    def test_payment_empty_order_fails(self):
        order = Order(customer_id="customer_123")
        self.order_repository.save(order)

        with pytest.raises(ValueError, match="Нельзя оплатить пустой заказ"):
            self.use_case.execute(order.id)

    def test_payment_twice_fails(self):
        order = Order(customer_id="customer_123")
        order.add_line("prod_1", "Товар 1", 1, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        self.use_case.execute(order.id)

        with pytest.raises(ValueError, match="Заказ уже оплачен"):
            self.use_case.execute(order.id)

    def test_cannot_modify_order_after_payment(self):
        order = Order(customer_id="customer_123")
        order.add_line("prod_1", "Товар 1", 1, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        self.use_case.execute(order.id)

        saved_order = self.order_repository.get_by_id(order.id)

        with pytest.raises(ValueError, match="Нельзя изменять оплаченный заказ"):
            saved_order.add_line("prod_2", "Товар 2", 1, Money(Decimal("50"), "USD"))