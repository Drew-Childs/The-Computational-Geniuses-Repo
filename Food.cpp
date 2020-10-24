#include "Food.h"

Food::Food() {
	food = "";
	recipe.resize(0);
	isFavorite = false;
}

Food::Food(string name, vector<ingred> recipe) {
	this->food = name;
	this->recipe = recipe;
	isFavorite = false;
}