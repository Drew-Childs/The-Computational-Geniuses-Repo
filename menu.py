from food import Food
import csv

def sortedDictionaryKeys(original_dict):
    # returns a sorted dictionary that is sorted by the keys
    sorted_dict = {}
    for i in range(len(original_dict)):
        largest_value = -1
        largest_word = ''
        for key, value in original_dict.items():
            if (original_dict[key] > largest_value) and (key not in sorted_dict):
                largest_value = value
                largest_word = key
        sorted_dict[largest_word] = largest_value
    return sorted_dict

def rebuildString(original_str):
    new_string = ""
    for x in original_str:
        if (x == "'") or (x == "[") or (x == "]"):
            continue
        new_string += x
    return new_string

class Menu:
    def __init__(self):
        self.foodList = []
        self.history = []
        self.shoppingCart = []
        self.allFavorites = []
        self.recommendedHistory = []

    def search(self, search):
        #self.history.append(search)
        keyWord = search.split()

        recipeSearchValue = {}
        for i in range(len(self.foodList)):  # iterates through all food items with recipes
            value = 0
            for k in range(len(keyWord)):
                for j in range(len(self.foodList[i].recipe)):  # iterates through a specific recipe
                    if keyWord[k].lower() in self.foodList[i].recipe[j].lower():
                        value += 1
                for j in range(len(self.foodList[i].tags)):
                    if j == 0 and k == 0:
                        if self.foodList[i].name.lower() in search.lower():
                            value += 5
                    elif keyWord[k].lower() in self.foodList[i].tags[j].lower():
                        value += 1

            if value > 0:
                recipeSearchValue[self.foodList[i]] = value

        sorted_recipeSearchValue = sortedDictionaryKeys(recipeSearchValue)

        return sorted_recipeSearchValue

    def readRecipes(self):
        with open('food.csv', 'r', encoding='utf-8') as csvfile:
            food_reader = csv.reader(csvfile, delimiter=',')

            for row in food_reader:
                old_recipe = row[6]
                new_recipe = rebuildString(old_recipe).split(',')

                old_tags = row[2]
                new_tags = rebuildString(old_tags).split(',')

                self.foodList.append(Food(row[0], row[1], new_tags, row[3], row[4], row[5], new_recipe, row[7], row[8], row[9]))

        # 0Name, 1Description, 2Tags, 3Prep Time, 4Cook Time, 5Servings, 6Recipe, 7Instructions, 8Picture, 9Author

    def recommendations(self):
        historyFreq = {}
        historyTags = []
        recommended = []
        for x in self.history:
            if x in historyFreq:
                historyFreq[x] += 1
            else:
                historyFreq[x] = 1

        sorted_historyFreq = sortedDictionaryKeys(historyFreq)

        for x in sorted_historyFreq:
            historyTags.append(x.tags)

        for x in self.foodList:
            for y in historyTags:
                if y in x.tags:
                    recommended.append(x)
                    break

        # want to only use the top 1 thru 3 for recommendations
        return recommended

    def createFood(self, name, recipe):
        self.foodList.append(Food(name, recipe))
        # doesn't save in csv

    def addToFavorites(self, food_item: Food):
        # food_item is of type food
        food_item.isFavorite = True
        self.allFavorites.append(food_item)

    def removeFavorite(self, food_item: Food):
        food_item.isFavorite = False
        if food_item in self.allFavorites:
            self.allIngredients.popitem()

    def printFavorites(self, results, tk):
        for x in self.allFavorites:
            results.insert(tk.END, x.name)

    def addToShoppingList(self, food_item: Food):
        self.allIngredients = {}  # dictionary of { ingredient : number of times it appears }
        self.shoppingCart.append(food_item)

    def printShoppingCart(self, results, tk):
        for x in self.shoppingCart:
            for y in x.recipe:
                results.insert(tk.END, y)

    def printHistory(self, results, tk):
        for x in self.history:
            results.insert(tk.END, x.name)



