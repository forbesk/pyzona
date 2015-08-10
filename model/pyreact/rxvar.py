
class RxVar:
    def __init__(self, value=None, valid=True):
        self.value = value
        self.valid = valid
        self.supplier = None
        self.consumers = []

    def set_supplier(self, supplier):
        self.supplier = supplier

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def validate(self):
        self.valid = True

    def invalidate(self):
        self.valid = False
        
        for consumer in self.consumers:
            consumer.sink.invalidate()
    
    def set(self, value):
        self.value = value
        
        for consumer in self.consumers:
            consumer.sink.invalidate()

    def get(self):
        if self.valid == False:
            if self.supplier != None:
                self.supplier.update()
                self.validate()
        return self.value
