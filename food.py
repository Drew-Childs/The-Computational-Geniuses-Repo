class ingred:
    def __init__(self, name="", amount=0, units=""):
        self.name = name
        self.amount = amount
        self.units = units  # type of unit for the given amount of ingredients


class Food:
    dishStyles = ["Breakfast", "Lunch", "Dinner", "Side Dish", "Appetizer", "Sandwich", "Dessert"]

    def __init__(self, name="", description="", tags=[], prepTime=0, cookTime=0, servings=0, recipe=[], instructions="",
                 pic="", author=""):
        # constructor
        self.name = name
        self.description = description
        self.tags = tags
        self.prepTime = prepTime
        self.cookTime = cookTime
        self.servings = servings
        self.recipe = recipe
        self.instructions = instructions
        self.pic = pic
        self.author = author

        self.isFavorite = False
        self.typeOfDish = ""

        for x in self.dishStyles:
            tags = [s.strip() for s in self.tags]
            if x.strip() in tags:
                self.typeOfDish = x
                break

        # self.nutrionValue = 0

        # note: the above would have to be implemented in the constructor to be part of each instance.

    # no need for getters/setters

