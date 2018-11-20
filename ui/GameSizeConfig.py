
def setUpSize():
    gameItemsSizes = {}
    # CharacterPage sizes
    gameItemsSizes[101002001] = ((32, 32), (64, 64), (128, 128))
    gameItemsSizes[101002002] = ((128, 128), (256, 256), (384, 384))
    # MasteriesPage
    gameItemsSizes[101003001] = ((32, 32), (64, 64), (128, 128))
    gameItemsSizes[101003002] = ((128, 128), (256, 256), (384, 384))
    # PerksPage
    gameItemsSizes[101004001] = ((32, 32), (64, 64), (128, 128))
    gameItemsSizes[101004002] = ((128, 128), (256, 256), (384, 384))
    # World size
    # Floor
    gameItemsSizes[102001001] = ((128, 128), (256, 256), (256, 256))
    # GameVision
    # Shaow
    gameItemsSizes[103001001] = ((128, 128), (256, 256), (256, 256))
    return gameItemsSizes

gameItemsSizes = setUpSize()