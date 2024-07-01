class BurnWires:
    def __init__(self) -> None:
        pass

    def duty_cycle(self, duty_cycle):
        assert 0 <= duty_cycle <= 0xFFFF
