import copy

class MonsterEquipment:

    def __init__(self, groups_sequence):
        """
        :param groups_sequence: collection of collections of items.
        use .new_sequence() to get a collection with a random choice from each of the groups.
        """
        corrected_seq = []
        for item in groups_sequence:
            try:
                iter(item)
            except TypeError:
                corrected_seq.append([item])
            else:
                corrected_seq.append(item)

        self.sequence = corrected_seq
        self.random = None

    def new_sequence(self, random):
        return [copy.deepcopy( random.choice(group) ) for group in self.sequence]

    def __iter__(self):
        return iter(self.new_sequence(self.random))

# if __name__ == "__main__":
#     me = MonsterEquipment([[1,2,3], 'abc', [2,3,7] ])
#
#     for _ in range(5):
#         print(me.new_sequence())
#
#     me = MonsterEquipment([[1, 2, 3], 'abc', [2, 3, 7], 555])
#
#     for _ in range(5):
#         print(me.new_sequence())
#
#     me = MonsterEquipment([[1, 2, 3], 'abc', [2, 3, 7]])
#
#     for _ in range(5):
#         print(list(me))
#
#     for item in me:
#         print(item)

