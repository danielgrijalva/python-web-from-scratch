from fields.charfield import CharField
from fields.numberfield import NumberField

class Product():
    model_name = 'product'

    def __init__(self):
        self.name = CharField()
        self.description = CharField()
        self.price = NumberField()
        self.stock = NumberField()
        self.columns = self.get_columns()

    def get_columns(self):
        columns = list(self.__dict__.keys())
        return columns
