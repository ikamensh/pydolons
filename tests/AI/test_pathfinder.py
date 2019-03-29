from mechanics.AI.pathfinding.astar_pathfinder import StarSearch
import pytest


@pytest.mark.timeout(50)
def test_finds_path(walls_game, hero):
    search = StarSearch(walls_game, hero)
    goal = 11 + 0j
    path = search.path_to(goal)
    assert path is not None
    assert 1.5 * len(path) >= walls_game.bf.distance(hero, goal)
