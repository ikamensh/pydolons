# from game_objects.battlefield_objects.CharAttributes import get_attrib_by_enum
# import pytest
# from exceptions import PydolonsError
#
#
# def test_can_up_attribs(char, var_attribute):
#     char.unit.xp = int(1e100)
#
#     before = get_attrib_by_enum(char.unit, var_attribute)
#
#     char.increase_attrib(var_attribute)
#
#     assert get_attrib_by_enum(char.unit, var_attribute) > before
#
# @pytest.mark.skip("Not implemented")
# def test_cant_up(char, var_attribute):
#     char.unit.xp = 0
#
#     with pytest.raises(PydolonsError):
#         char.increase_attrib(var_attribute)
#
# @pytest.mark.skip("Not implemented")
# def test_cant_down_other(char, var_attribute):
#     char.unit.xp = int(1e100)
#
#     with pytest.raises(PydolonsError):
#         char.increase_attrib(var_attribute)
#
#
# def test_reset(char, var_attribute):
#     char.unit.xp = int(1e100)
#
#     before = get_attrib_by_enum(char.unit, var_attribute)
#
#     char.increase_attrib(var_attribute)
#
#     assert get_attrib_by_enum(char.unit, var_attribute) > before
#
#     char.reset()
#
#     assert get_attrib_by_enum(char.unit, var_attribute) == before
#
#
# def test_commit(char, var_attribute):
#     char.unit.xp = int(1e100)
#
#     before = get_attrib_by_enum(char.unit, var_attribute)
#
#     char.increase_attrib(var_attribute)
#
#     assert get_attrib_by_enum(char.unit, var_attribute) > before
#
#     char.commit()
#     char.reset()
#
#     assert get_attrib_by_enum(char.unit, var_attribute) > before
#
#
#
#
#
#
#
#
#
#
#
#
#
