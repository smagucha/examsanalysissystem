class classdecorator:
    def __init__(self, inputfunction):
        self.inputfunction = inputfunction

    # def decorator(self):
    #     result = self.inputfunction()
    #     resultdecorator = " decorated by a class decorator"
    #     return result + resultdecorator

    def __call__(self):
        result = self.inputfunction()
        resultdecorator = " decorated by a class decorator"
        return result + resultdecorator


@classdecorator
def inputfunction():
    return "This is input function"


print(inputfunction())
