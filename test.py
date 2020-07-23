
# 3 pillars of OOPS:
#     -Inheritance
#     -Encapsulation (private, public, protected)
#     -Polymorphism


class Mammal:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def _mate(self):
        print('mates with opposite sex')


class Human(Mammal):

    # protected member starts with _ (just the agreed convention)
    # private member start with __ (python throws error if allowed)

    def __init__(self, name, dumb):
        super().__init__('ansuman')
        self.dumb = dumb
        print('initialize the human class')

    def __speak(self):
        print('speaking')

    def walk(self):
        print('walking')

    def can_it_speak(self):
        if not self.dumb:
            print('yes')
            self.__speak()
        else:
            print('no')

    def __str__(self):
        return super().__str__() + ' also a human'


human = Human(name='Ansuman', dumb=False)
print(human._mate())
print(human)
# human.walk()
# human.can_it_speak()
