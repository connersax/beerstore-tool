class Beer:
    def __init__(self, name: str, quantity: int, type: str, serving: int,  price: float, stock, onSale):
        self.name = name
        self.quantity = quantity
        self.type = type
        self.serving = serving  # in ml
        self.price = price
        self.stock = stock
        self.__inStock__ = stock != 0
        self.onSale = onSale

    def __lt__(self, obj):
        return self.mlPerDollar() < obj.mlPerDollar()

    def __gt__(self, obj):
        return self.mlPerDollar() > obj.mlPerDollar()

    def __le__(self, obj):
        return self.mlPerDollar() <= obj.mlPerDollar()

    def __ge__(self, obj):
        return self.mlPerDollar() >= obj.mlPerDollar()
    
    def __eq__(self, obj):
        return self.mlPerDollar() == obj.mlPerDollar()

    def dollarPerMl(self) -> float:
        return self.price / float(self.quantity) * float(self.serving)

    def mlPerDollar(self) -> float:
        return float(self.quantity) * float(self.serving) / self.price
