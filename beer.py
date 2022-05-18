class Beer:
    def __init__(self, name: str, quantity: int, type: str, servingMl: int,  price: float, stock: int, onSale: bool):
        self.name = name
        self.quantity = quantity
        self.type = type
        self.servingMl = servingMl
        self.price = price
        self.stock = stock
        self.onSale = onSale

    def __str__(self) -> str:
        out_msg = (
            f'{self.name}{" (On Sale)" if self.onSale else ""}\n'
            f'{self.quantity} {self.type} \u00d7 {self.servingMl}ml at ${self.price:.2f}\n'
            f'{self.mlPerDollar():.2f}ml/$\n'
        )
        return out_msg

    def __lt__(self, obj):
        if isinstance(obj, Beer):
            return self.mlPerDollar() < obj.mlPerDollar()
        return False

    def __gt__(self, obj):
        if isinstance(obj, Beer):
            return self.mlPerDollar() > obj.mlPerDollar()
        return False

    def __le__(self, obj):
        if isinstance(obj, Beer):
            return self.mlPerDollar() <= obj.mlPerDollar()
        return False

    def __ge__(self, obj):
        if isinstance(obj, Beer):
            return self.mlPerDollar() >= obj.mlPerDollar()
        return False

    def __eq__(self, obj):
        if isinstance(obj, Beer):
            return self.mlPerDollar() == obj.mlPerDollar()
        return False

    def inStock(self) -> bool:
        return self.stock != 0

    def dollarPerMl(self) -> float:
        return self.price / float(self.quantity) * float(self.servingMl)

    def mlPerDollar(self) -> float:
        return float(self.quantity) * float(self.servingMl) / self.price
