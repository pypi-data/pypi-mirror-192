from .subpkg.submoduleone import SubOne
from .subpkg.submoduletwo import SubTwo

class MainClass:
    def __init__(self,name):
        self.name = name

    def delegate_implementations(self):
        objOne = SubOne()
        objTwo = SubTwo()

        objOne.say_hello()
        objTwo.say_hello()


if __name__ == '__main__':
    exec = MainClass("mainentry executed..")
    exec.delegate_implementations()