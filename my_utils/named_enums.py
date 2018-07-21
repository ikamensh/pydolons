from enum import Enum, auto

class NameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
       return name

    def __repr__(self):
        return self.name.capitalize()






if __name__ == "__main__":
    class Ordinal(NameEnum):
        NORTH = auto()
        SouthWest = auto()
        East = auto()
        West = auto()


    print(list(Ordinal))