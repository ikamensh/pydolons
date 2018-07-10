from DreamGame import DreamGame

def cell_to_unit(cell_targeting):
    return DreamGame.get_unit_at(cell_targeting.cell)

def same_unit_as_targeted(unit_targeting):
    return unit_targeting.unit

def all_in_aoe_around_cell(max_dist):
    def targeting_factory(cell_targeting):
        return [u for u, dist in DreamGame.get_units_distances_from(cell_targeting.cell)
                if dist <= max_dist]
    return targeting_factory
