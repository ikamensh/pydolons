from battlefield import Cell
import pytest

@pytest.mark.parametrize('vec', [1+0j, 1j, 1e9j, 1e-12 + 1e-12j])
def test_zero_to_self(vec):
    assert Cell.angle_between(vec, vec)[0] == 0

@pytest.mark.parametrize('vectors_ccw',
                           [   (-1j, 1+0j, False),
                               (-1j, 1-0j, False),
                               (-1j, 1 - 2j, False),
                               (-1j, -1+0j, True),
                               (-1j, -1-0j, True)])
def test_ccw_cw(vectors_ccw):

    v1, v2, ccw_bool = vectors_ccw
    assert Cell.angle_between(v1, v2)[1] is ccw_bool

def test_comlex():
    # print(complex(0, -1))
    N = (0 - 1j)
    W = (-1 + 0j)
    S = (0 + 1j)
    E = (1 + 0j)

    assert Cell.from_complex(N) == Cell(0, 0)
    assert Cell.from_complex(W) == Cell(0, 0)
    assert Cell.from_complex(S) == Cell(0, 1)
    assert Cell.from_complex(E) == Cell(1, 0)

