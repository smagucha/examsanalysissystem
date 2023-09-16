class MetaClass(type):
    def __new__(self, name, base, dct):
        obj = super().__new__(self, name, base, dct)
        obj.attribute = 10
        return obj


# MetaClass acts as template for CustomClass
class CustomClass(metaclass=MetaClass):
    pass


print(CustomClass.attribute)
