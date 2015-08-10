class RxFunc:
    def __init__(self, func=None, sink=None, sources=None):
        self.func = func
        self.sink = sink
        self.sources = sources
    
    def update(self):
        for source in self.sources:
            if source.supplier != None:
                source.supplier.update()

        self.sink.value = self.func()
