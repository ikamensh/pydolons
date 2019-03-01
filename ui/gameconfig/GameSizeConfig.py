
def setUpSize():
    gameItemsSizes = {}
    # CharacterPage sizes
    gameItemsSizes[101002001] = ((32, 32), (64, 64), (96, 96))
    gameItemsSizes[101002002] = ((128, 128), (152, 152), (256, 256))
    # MasteriesPage
    gameItemsSizes[101003001] = ((32, 32), (64, 64), (96, 96))
    gameItemsSizes[101003002] = ((128, 128), (256, 256), (384, 384))
    # PerksPage
    gameItemsSizes[101004001] = ((32, 32), (64, 64), (96, 96))
    gameItemsSizes[101004002] = ((128, 128), (256, 256), (384, 384))
    # InventoryPage
    gameItemsSizes[101005001] = ((64, 64), (64, 64), (64, 64))
    gameItemsSizes[101005002] = ((128, 128), (256, 256), (384, 384))
    # World size
    # Floor
    gameItemsSizes[102001001] = ((128, 128), (128, 128), (128, 128))
    # GameVision
    # Shaow
    gameItemsSizes[103001001] = ((128, 128), (128, 128), (128, 128))
    return gameItemsSizes

gameItemsSizes = setUpSize()

