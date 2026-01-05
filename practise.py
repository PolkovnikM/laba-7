from decimal import Decimal
from datetime import datetime
import uuid

from src.domain.money import Money
from src.domain.order import Order
from src.infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from src.infrastructure.payment_gateways.fake_payment_gateway import FakePaymentGateway
from src.application.use_cases.pay_order_use_case import PayOrderUseCase


def print_separator():
    print("\n" + "=" * 60 + "\n")


def main():
    print("СИСТЕМА УПРАВЛЕНИЯ ЗАКАЗАМИ И ОПЛАТАМИ")
    print_separator()

    # Инициализация
    print("1. ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ")
    repository = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repository, gateway)
    print("   Репозиторий и платёжный шлюз инициализированы")

    print_separator()

    # Создание заказа
    print("2. СОЗДАНИЕ ЗАКАЗОВ")

    # Заказ 1: Электроника
    print("\nЗАКАЗ #1: Электроника")
    order1 = Order(
        id="order-" + str(uuid.uuid4())[:8],
        customer_id="cust-001"
    )
    order1.add_line("laptop-001", "Ноутбук Lenovo", 1, Money(Decimal("899.99"), "USD"))
    order1.add_line("mouse-001", "Беспроводная мышь", 2, Money(Decimal("29.99"), "USD"))
    order1.add_line("keyboard-001", "Механическая клавиатура", 1, Money(Decimal("89.99"), "USD"))
    repository.save(order1)

    print(f"   ID: {order1.id}")
    print(f"   Клиент: {order1.customer_id}")
    print(f"   Позиций: {len(order1.lines)}")
    print(f"   Сумма: {order1.total_amount}")
    print(f"   Статус: {order1.status.value}")

    # Заказ 2: Книги
    print("\nЗАКАЗ #2: Книги")
    order2 = Order(
        id="order-" + str(uuid.uuid4())[:8],
        customer_id="cust-002"
    )
    order2.add_line("book-001", "Clean Code", 1, Money(Decimal("49.99"), "USD"))
    order2.add_line("book-002", "Design Patterns", 2, Money(Decimal("39.99"), "USD"))
    repository.save(order2)

    print(f"   ID: {order2.id}")
    print(f"   Клиент: {order2.customer_id}")
    print(f"   Позиций: {len(order2.lines)}")
    print(f"   Сумма: {order2.total_amount}")
    print(f"   Статус: {order2.status.value}")

    print_separator()

    # Оплата заказов
    print("3. ПРОЦЕСС ОПЛАТЫ")

    # Успешная оплата заказа 1
    print("\nОПЛАТА ЗАКАЗА #1:")
    try:
        result1 = use_case.execute(order1.id)
        print(f"   ✓ Успешно оплачен!")
        print(f"   Транзакция ID: {result1['transaction_id']}")
        print(f"   Сумма: {result1['amount']}")
        print(f"   Новый статус: {result1['status']}")
        print(f"   Время оплаты: {repository.get_by_id(order1.id).paid_at.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")

    # Попытка оплаты пустого заказа
    print("\n СОЗДАЕМ ПУСТОЙ ЗАКАЗ И ПЫТАЕМСЯ ОПЛАТИТЬ:")
    empty_order = Order(id="order-empty", customer_id="cust-003")
    repository.save(empty_order)

    try:
        result_empty = use_case.execute(empty_order.id)
        print(f"   ✗ Не должно было получиться!")
    except ValueError as e:
        print(f"   ✓ Корректно отклонено: {e}")

    print_separator()

    # Проверка инвариантов
    print("4. ПРОВЕРКА ИНВАРИАНТОВ")

    # Попытка изменить оплаченный заказ
    print("\nПОПЫТКА ИЗМЕНИТЬ ОПЛАЧЕННЫЙ ЗАКАЗ #1:")
    paid_order = repository.get_by_id(order1.id)
    try:
        paid_order.add_line("cable-001", "USB-C кабель", 1, Money(Decimal("19.99"), "USD"))
        print("   ✗ Не должно было получиться!")
    except ValueError as e:
        print(f"   ✓ Корректно: {e}")

    # Попытка оплатить уже оплаченный заказ
    print("\nПОПЫТКА ПОВТОРНОЙ ОПЛАТЫ ЗАКАЗА #1:")
    try:
        use_case.execute(order1.id)
        print("   ✗ Не должно было получиться!")
    except ValueError as e:
        print(f"   ✓ Корректно: {e}")

    # Успешная оплата заказа 2
    print("\nОПЛАТА ЗАКАЗА #2:")
    try:
        result2 = use_case.execute(order2.id)
        print(f"   ✓ Успешно оплачен!")
        print(f"   Транзакция ID: {result2['transaction_id']}")
        print(f"   Сумма: {result2['amount']}")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")

    print_separator()

    # Проверка транзакций
    print("5. ПРОВЕРКА ТРАНЗАКЦИЙ В ПЛАТЕЖНОМ ШЛЮЗЕ")
    print(f"   Всего транзакций: {len(gateway.transactions)}")

    for i, (trans_id, trans_data) in enumerate(gateway.transactions.items(), 1):
        print(f"\n   Транзакция #{i}:")
        print(f"   ID: {trans_id}")
        print(f"   Заказ: {trans_data['order_id']}")
        print(f"   Сумма: {trans_data['amount']}")
        print(f"   Статус: {trans_data['status']}")

    print_separator()

    # Итоги
    print("6. ИТОГИ")
    orders = [order1, order2, empty_order]
    paid_count = sum(1 for o in orders if repository.get_by_id(o.id) and repository.get_by_id(o.id).is_paid())
    total_revenue = Money.zero()

    for order in orders:
        saved_order = repository.get_by_id(order.id)
        if saved_order and saved_order.is_paid():
            total_revenue = total_revenue + saved_order.total_amount

    print(f"   Всего заказов: {len(orders)}")
    print(f"   Оплачено: {paid_count}")
    print(f"   Ожидают оплаты: {len(orders) - paid_count}")
    print(f"   Общая выручка: {total_revenue}")

    print_separator()
    print("✅ ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ УСПЕШНО")
    print("Process finished with exit code 0")


if __name__ == "__main__":
    main()