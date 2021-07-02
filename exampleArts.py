import classes

# (self, name, mods, cc, mv, rg, cost, atkType = 'PHY') -- cc - crowd control, mv - player movement, rg - range
pierce = classes.Art('Pierce', [['DEF', 0.5], ['DEX', 1.1]], 'F', 'F', ['F'], 15)

broadSlash = classes.Art('Broad Slash', [['ATK', 1.2], ['DEX', 0.9]], 'R', '', ['FL','F','FR'], 20)

greatPierce = classes.Art('Great Pierce', [['DEF', 0.25], ['DEX', 1.2]], 'FF', 'F', ['F', 'FF'], 25)

autumn = classes.Art('Autumn Leaf', [['DEF', 0.5], ['DEX', 1.2]], 'F', 'FFFF', ['F', 'FL', 'FR', 'FF', 'FFL', 'FFR'], 20)

arcSlash = classes.Art('Arc Slash', [['ATK', 2]], 'F', '', ['F', 'FF', 'FFL', 'FFR', 'FFF', 'FFFF', 'FFFFF'], 30)

gale = classes.Art('Gale', [['ATK', 1.2], ['DEF', 0.75]], 'F', 'FFF', ['FFF', 'FFFF'], 25)

runeBlade = classes.Art('Rune Blade', [['INT', 1.5]], 'R', 'F', ['F', 'FR'], 20, atkType='MAG')

pierceStep = classes.Art('Pierce Step', [['DEF', 0.5], ['DEX', 1.1]], '', 'F', ['FF'], 20)

leftSlash = classes.Art('Left Slash', [['ATK', 1.1]], 'L', 'F', ['FL'], 20)

pullSlash = classes.Art('Pull Slash', [['AGI', 0.5]], 'B', '', ['FF'], 20)

step = classes.Art('Step', [], '', 'F', [], 10)

allArts = [pierce, broadSlash, greatPierce, autumn, arcSlash, gale, runeBlade, pierceStep, leftSlash, pullSlash, step]