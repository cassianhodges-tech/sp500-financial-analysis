class Wing(object):

    def __init__(self, ratio):
        self.ratio = ratio

    def fly(self):
        if self.ratio > 1:
            print("Weee, this is fun")
        elif self.ratio == 1:
            print("This is hard work, but I'm flying")
        else:
            print("I think I'll just walk")

    @classmethod
    def sing(cls):
        print('ATTACK')

    @staticmethod
    def mate():
        print('told ya')
duck = Wing(1.9)  #Calling method on permanent object instantiation
duck.fly()
duck.sing()
Wing.sing()       #Calling method on class
Wing(1.5).sing()
Wing(1).mate()
Wing().sing()
Wing().mate()

