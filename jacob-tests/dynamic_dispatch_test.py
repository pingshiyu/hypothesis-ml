class BaseC:
    def __init__(self):
        super().__init__()
        print(f"{self.secret_str}.__init__ of BaseC")

    @property
    def secret_str(self) -> str:
        return "BaseC"

class SuperC(BaseC):
    @property
    def secret_str(self) -> str:
        return "SuperC"

if __name__ == '__main__':
    o = SuperC() # expect "SuperC.__init__ of BaseC"