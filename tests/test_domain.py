import pytest
from decimal import Decimal
from src.domain.money import Money
from src.domain.order import Order
from src.domain.order_status import OrderStatus


class TestMoney:

    def test_create_money(self):
        money = Money(Decimal("100.50"), "USD")
        assert money.amount == Decimal("100.50")
        assert money.currency == "USD"

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError):
            Money(Decimal("-10"), "USD")

    def test_empty_currency_raises_error(self):
        with pytest.raises(ValueError):
            Money(Decimal("100"), "")

    def test_addition(self):
        money1 = Money(Decimal("100"), "USD")
        money2 = Money(Decimal("50"), "USD")
        result = money1 + money2
        assert result.amount == Decimal("150")

    def test_addition_different_currencies_raises_error(self):
        money1 = Money(Decimal("100"), "USD")
        money2 = Money(Decimal("50"), "EUR")
        with pytest.raises(ValueError):
            money1 + money2

    def test_zero_factory(self):
        zero = Money.zero("USD")
        assert zero.amount == Decimal("0")
        assert zero.currency == "USD"
        assert zero.is_zero()


class TestOrder:

    def test_create_order(self):
        order = Order(customer_id="customer_123")
        assert order.customer_id == "customer_123"
        assert order.status == OrderStatus.CREATED
        assert order.is_empty()
        assert not order.is_paid()

    def test_empty_order_total(self):
        order = Order(customer_id="customer_123")
        assert order.total_amount.amount == Decimal("0")

    def test_add_line(self):
        order = Order(customer_id="customer_123")
        price = Money(Decimal("100"), "USD")

        order.add_line("prod_1", "Товар 1", 2, price)

        assert len(order.lines) == 1
        assert order.total_amount.amount == Decimal("200")

    def test_cannot_modify_paid_order(self):
        order = Order(customer_id="customer_123")
        price = Money(Decimal("100"), "USD")
        order.add_line("prod_1", "Товар 1", 1, price)
        order.pay()

        with pytest.raises(ValueError, match="Нельзя изменять оплаченный заказ"):
            order.add_line("prod_2", "Товар 2", 1, price)

    def test_cannot_pay_empty_order(self):
        order = Order(customer_id="customer_123")

        with pytest.raises(ValueError, match="Нельзя оплатить пустой заказ"):
            order.pay()

    def test_cannot_pay_twice(self):
        order = Order(customer_id="customer_123")
        price = Money(Decimal("100"), "USD")
        order.add_line("prod_1", "Товар 1", 1, price)
        order.pay()

        with pytest.raises(ValueError, match="Заказ уже оплачен"):
            order.pay()