function showRecipe(recipeName) {
    var recipeTitle = document.querySelector('.recipe-title');
    var recipeInstructions = document.querySelector('.recipe-instruct p');
    
    // Find the recipe object from the recipe list
    var recipe = recipe_list.find(function(item) {
        return item.name === recipeName;
    });
    
    // Update the recipe details
    recipeTitle.textContent = recipe.name;
    recipeInstructions.textContent = recipe.instructions;
}