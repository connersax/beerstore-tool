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
        self.dollarPerMl = self.price / float(self.quantity) * float(self.serving)
        self.mlPerDollar = float(self.quantity) * float(self.serving) / self.price

    def sortBy(self):
        return self.mlPerDollar
