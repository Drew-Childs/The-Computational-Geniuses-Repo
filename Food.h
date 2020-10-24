#pragma once
#include <string>
#include <vector>
#include <list>
#include <iostream>

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
	Food(string name, vector<ingred> recipe);

	void setItemName(string Name) { food = Name; }
	string getItemName() { return food; }

	void addIngredient(ingred ingredient) { recipe.push_back(ingredient); }
	vector<ingred> getRecipe() { return recipe; }

	void setKeyWords(vector<string> key) { keyWords = key; }
	void addKeyWords(string key) { keyWords.push_back(key); }
	vector<string> getKeyWords() { return keyWords; }

	void setFavorite(bool status) { isFavorite = status; }
	bool getFavorite() { return isFavorite; }

private:
	string food;
	vector<ingred> recipe;
	vector<string> keyWords;
	bool isFavorite;
	double nutritionValue;
};