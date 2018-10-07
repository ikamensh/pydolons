from battlefield import Cell

def test_angles():
    q1 = 1 + 1j
    q2 = -1 + 1j
    q3 = -1 - 1j
    q4 = 1 - 1j

    assert Cell.angle_between(q1, q2) == (90, False)
    assert Cell.angle_between(q3, q4) == (90, False)
    assert Cell.angle_between(q4, q3) == (90, True)

    assert Cell.angle_between(q1, q3)[0] == 180
    assert Cell.angle_between(q2, q4)[0] == 180

    assert Cell.angle_between(q3, q2) == (90, True)
    assert Cell.angle_between(q1, q4) == (90, False)

    q1 -= 0.5j
    q2 -= 0.5j

    q3 += 0.5j
    q4 += 0.5j

    assert Cell.angle_between(q1, q2) > (90, False)
    assert Cell.angle_between(q3, q4) > (90, False)
    assert Cell.angle_between(q4, q3) > (90, True)

    assert Cell.angle_between(q1, q3)[0] == 180
    assert Cell.angle_between(q2, q4)[0] == 180

    assert Cell.angle_between(q3, q2) < (90, True)
    assert Cell.angle_between(q1, q4) < (90, False)