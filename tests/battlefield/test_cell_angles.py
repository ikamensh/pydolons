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

def test_angles():
    q1 = 1 - 1j
    q2 = -1 - 1j
    q3 = -1 + 1j
    q4 = 1 + 1j

    assert Cell.angle_between(q1, q2) == (90, True)
    assert Cell.angle_between(q3, q4) == (90, True)
    assert Cell.angle_between(q4, q3) == (90, False)

    assert Cell.angle_between(q1, q3)[0] == 180
    assert Cell.angle_between(q2, q4)[0] == 180

    assert Cell.angle_between(q3, q2) == (90, False)
    assert Cell.angle_between(q1, q4) == (90, False)

    q1 += 0.5j
    q2 += 0.5j

    q3 -= 0.5j
    q4 -= 0.5j

    assert Cell.angle_between(q1, q2) > (90, True)
    assert Cell.angle_between(q3, q4) > (90, True)
    assert Cell.angle_between(q4, q3) > (90, False)

    assert Cell.angle_between(q1, q3)[0] == 180
    assert Cell.angle_between(q2, q4)[0] == 180

    assert Cell.angle_between(q3, q2) < (90, False)
    assert Cell.angle_between(q1, q4) < (90, False)