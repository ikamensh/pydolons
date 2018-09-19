import math

class GameMath(object):
    """docstring for GameMath."""
    def __init__(self):
        super(GameMath, self).__init__()

    @staticmethod
    def get_direction(x, y):
        """Метод возвращет направление по текущим координатам относительно
        центра
        """
        dVectors = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
        deg = int(math.degrees(math.atan2(x, y)))

        if x == 0 and y == 0:
            return dVectors[0]
        elif (x, y) is dVectors:
            return x, y
        elif deg < 22 and deg > -22:
            return 0, 1
            # print('S')
        elif deg < 68 and deg > 23:
            return 1, 1
            # print('SW')
        elif deg < 112 and deg > 67:
            return 1, 0
            # print('W')
        elif deg < 157 and deg > 111:
            return 1, -1
            # print('NW')
        elif deg < -156 or deg > 156:
            return 0, -1
            # print('N')
        elif deg < -111  and deg > -157:
            return -1, -1
            # print('NO')
        elif deg < -67  and deg > -112:
            return -1, 0
            # print('O')
        elif deg < -22  and deg > -68:
            return -1, 1
            # print('SO')
        # print(int(math.degrees(at)))

    @staticmethod
    def getTranslate(x1, y1, x2, y2):
        """Смещение относительно точки х1, у1
        в начало координат для вычисления направления
        """
        return x2 + (x1 * -1), y2 + (y1 * -1)

    # @staticmethod
    # def get_lenght_hp(hp)
