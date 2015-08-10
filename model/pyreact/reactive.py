from rxfunc import RxFunc

class Reactive:
    def __init__(self):
        pass

    def connect(self, sink, sources, func):
        rxfunc = RxFunc(func, sink, sources)

        sink.set_supplier(rxfunc)

        for source in sources:
            source.add_consumer(rxfunc)
            source.invalidate()

        rxfunc.update()
