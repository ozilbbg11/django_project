

word = "['80g/3oz salt', '1 tsp coriander seeds', '1 tsp fennel seeds', '2 star anise', '1 tbsp roughly chopped stem ginger', '250g/9oz pork chops, trimmed', '350g/12oz dried apricots', '175g/6oz raisins', '7g/¼oz black mustard seeds', '7g/¼oz white mustard seeds', '250g/9oz caster sugar', '375ml/13fl oz cider vinegar', '100g/3½oz ground almonds', 'handful dried apricots, finely chopped', '1 red chilli, finely chopped', 'handful fresh coriander leaves', '½ mooli, thinly sliced', '½ black radish, thinly sliced', '10 breakfast radishes, thinly sliced', 'olive oil, for drizzling', 'salt and freshly ground black pepper', 'watercress, to serve']"

s = word.replace("'", '').replace(']', '').replace('[', '')

print(s)

