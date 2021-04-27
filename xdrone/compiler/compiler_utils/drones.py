import copy


class DroneIdentifier:
    def __init__(self, ident: str):
        self._ident = ident

    @property
    def ident(self) -> str:
        return copy.deepcopy(self._ident)

    def __str__(self):
        return "DroneIdentifier: {{ ident: {} }}".format(self._ident)

    def __eq__(self, other):
        if isinstance(other, DroneIdentifier):
            return other._ident == self._ident
        return False
