class ClassWithProperties:
    privateValue = 'Can not be changed'
    def expose(self):
        print(self.privateValue)


def closure():
    privateValue = 'In a closure, it can not be changed'
    def expose():
        print privateValue

    return expose  ## Returns a function


instance = ClassWithProperties()
instance.expose()
instance.privateValue = 'But it was changed'
instance.expose()


closureResult = closure()
closureResult()
closureResult.privateValue = 'This change will not work'
closureResult()