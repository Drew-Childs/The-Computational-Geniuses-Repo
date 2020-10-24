#pragma once
#include <string>
#include <vector>

using namespace std;


struct ingred {

	string name;
	double amount;
	string type;
	
	ingred() {
		name = "";
		amount = 0;
		type = "";
	}
};



class Food {

public:
	Food();
	Food(string food);
	Food(string name, vector<ingred> recipe);

	void setItemName(string Name) { food = Name; }
	string getItemName() { return food; }

	void addIngredient(ingred ingredient) { recipe.push_back(ingredient); }
	vector<ingred> getRecipe() { return recipe; }

private:
	string food;
	vector<ingred> recipe;
};