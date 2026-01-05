from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass(frozen=True)
class Money:
    """Value Object для денег"""
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < Decimal("0"):
            raise ValueError("Сумма не может быть отрицательной")
        if not self.currency:
            raise ValueError("Валюта обязательна")

    def __add__(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise ValueError("Нельзя складывать разные валюты")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise ValueError("Нельзя вычитать разные валюты")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: Decimal | int) -> Self:
        return Money(self.amount * Decimal(str(multiplier)), self.currency)

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    @classmethod
    def zero(cls, currency: str = "USD") -> Self:
        return cls(Decimal("0"), currency)

    @classmethod
    def from_int(cls, amount: int, currency: str = "USD") -> Self:
        return cls(Decimal(str(amount)), currency)

    def is_positive(self) -> bool:
        return self.amount > Decimal("0")

    def is_zero(self) -> bool:
        return self.amount == Decimal("0")