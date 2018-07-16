
def test_create_blueprint(my_sword_blueprint):
    assert my_sword_blueprint.damage is not None

def test_create_item(bronze, usual, my_sword_blueprint):
    my_sword = my_sword_blueprint.to_item(bronze, usual)

    assert my_sword.damage.amount < my_sword_blueprint.damage.amount

def test_quality_matters(bronze, usual, legendary, my_sword_blueprint):
    sword1 = my_sword_blueprint.to_item(bronze, usual)
    sword2 = my_sword_blueprint.to_item(bronze, legendary)

    assert sword1.damage.amount < sword2.damage.amount