
def setUpSize():
    gameItemsSizes = {}
    # CharacterPage sizes
    gameItemsSizes[101002001] = ((32, 32), (64, 64), (128, 128))
    gameItemsSizes[101002002] = ((128, 128), (256, 256), (384, 384))
    # MasteriesPage
    gameItemsSizes[101003001] = ((32, 32), (64, 64), (128, 128))
    gameItemsSizes[101003002] = ((128, 128), (256, 256), (384, 384))
    return gameItemsSizes

gameItemsSizes = setUpSize()