
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    name: str


@dataclass
class Order:
    order_id: int
    user_id: int
    amount: float


@dataclass
class OrderResult:
    success: bool
    message: str
    total: float = 0.0


class UserRepository:
    def __init__(self):
        self.users = {
            101: User(101, "Aarav"),
            102: User(102, "Diya"),
            103: User(103, "Kabir"),
        }

    def get_user(self, user_id: int) -> User | None:
        return self.users.get(user_id)


class OrderService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def calculate_total(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Order amount must be positive")
        return round(amount * 1.18, 2)

    def create_order(self, order: Order) -> OrderResult:
        user = self.user_repository.get_user(order.user_id)

        if user is None:
            return OrderResult(False, "User not found")

        total = self.calculate_total(order.amount)

        return OrderResult(
            success=True,
            message=f"Order {order.order_id} created for {user.name}",
            total=total,
        )


def build_demo_service() -> OrderService:
    repository = UserRepository()
    return OrderService(repository)


def main():
    service = build_demo_service()

    valid_order = Order(order_id=5001, user_id=101, amount=250.0)
    print(service.create_order(valid_order))

    # Deliberate runtime bug for testing the self-healing pipeline.
    broken_order = service.create_order(103)
    print(broken_order)


if __name__ == "__main__":
    main()
