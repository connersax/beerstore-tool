class Beer:
    name: str
    quantity: int
    type: str
    price: float
    stock: None
    inStock: bool
    onSale: bool
    dollarPerMl: float
    mlPerDollar: float

    def __init__(self, name: str, quanTypeStr: str, price: float, stock, onSale):
        self.name = name
        delimitedStr = quanTypeStr.split(" ")
        self.quantity = int(delimitedStr[0])
        self.type = delimitedStr[2]
        self.serving = int(delimitedStr[3])  # in ml
        self.price = price
        self.stock = stock
        self.inStock = False if stock == 0 else True
        self.onSale = onSale
        self.dollarPerMl = self.price / float(self.quantity * self.serving)
        self.mlPerDollar = float(self.quantity * self.serving) / self.price

    def sortBy(self):
        return self.mlPerDollar
