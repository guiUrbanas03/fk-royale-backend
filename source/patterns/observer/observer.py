class Observer:
    def __init__(self) -> None:
        self.observers = []

    def observe(self, observer_function):
        self.observers.append(observer_function)

    def notify_all(self, data: dict):
        for observer in self.observers:
            observer(data)
