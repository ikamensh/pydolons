
def test_create_blueprint(my_sword_blueprint):
    assert my_sword_blueprint.name is not None


def test_create_item(bronze, silver, usual, my_sword_blueprint):
    my_sword1 = my_sword_blueprint.to_item(bronze, usual, game=None)
    my_sword2 = my_sword_blueprint.to_item(silver, usual, game=None)

    assert my_sword1.damage.amount < my_sword2.damage.amount


def test_quality_matters(bronze, usual, legendary, my_sword_blueprint):
    sword1 = my_sword_blueprint.to_item(bronze, usual, game=None)
    sword2 = my_sword_blueprint.to_item(bronze, legendary, game=None)

    assert sword1.damage.amount < sword2.damage.amount
