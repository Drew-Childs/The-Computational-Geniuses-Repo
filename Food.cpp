#include "Food.h"

Food::Food() {
	food = "";
	recipe.resize(0);
}

Food::Food(string food) {
	this->food = food;
	recipe.resize(0);
}

Food::Food(string name, vector<ingred> recipe) {
	this->food = name;
	this->recipe = recipe;
}