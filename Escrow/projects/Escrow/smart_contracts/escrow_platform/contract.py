from algopy import ARC4Contract, arc4


class EscrowPlatform(ARC4Contract):
    @arc4.abimethod()
    def hello(self, name: arc4.String) -> arc4.String:
        return "Hello, " + name
