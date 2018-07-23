from my_utils.named_enums import NameEnum


class Facing(NameEnum):

    NORTH = (0 + 1j)
    WEST = (-1 + 0j)
    SOUTH = (0 - 1j)
    EAST = (1 + 0j)


class FacingUtil:
    f = Facing
    from_complex = {(0 + 1j): f.NORTH,
                    (-1 + 0j): f.WEST,
                    (0 - 1j): f.SOUTH,
                    (1 + 0j): f.EAST}
    to_complex = {v: k for k, v in from_complex.items()}

    @staticmethod
    def coord_to_complex(cell):
        return cell.x + cell.y*1j