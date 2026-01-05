# Лабораторная работа 7: Архитектура, слои и DDD-lite

## Описание проекта
Система оплаты заказов с использованием DDD-lite и слоистой архитектуры. Проект демонстрирует разделение ответственности между слоями: Domain, Application, Infrastructure и Tests.

## Архитектура

### Слоистая структура (Clean Architecture + DDD-lite)
order-payment-system/
├── domain/ # Бизнес-логика и доменная модель
├── application/ # Use Cases и интерфейсы (Ports)
├── infrastructure/ # Реализации интерфейсов
└── tests/ # Модульные тесты
