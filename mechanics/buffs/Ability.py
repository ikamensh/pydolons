class Ability:
    def __init__(self, attributes_dict):
        self.attributes_dict = attributes_dict

    def __getitem__(self, item):
        return self.attributes_dict.get(item, None)