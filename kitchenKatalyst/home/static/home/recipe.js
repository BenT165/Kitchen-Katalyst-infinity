const searchBtn = document.getElementById('search-btn');
const mealList = document.getElementById('meal');
const mealDetailsContent = document.querySelector('.meal-details-content');
const recipeCloseBtn = document.getElementById('recipe-close-btn');

// Event listeners
searchBtn.addEventListener('click', getMealList);
mealList.addEventListener('click', getMealRecipe);
recipeCloseBtn.addEventListener('click', () =>{
    mealDetailsContent.parentElement.classList.remove('showRecipe');
});

// Get meal list that matches with the ingredients
function getMealList() {
    let searchInputTxt = document.getElementById('search-input').value.trim();
    fetch(`https://www.themealdb.com/api/json/v1/1/search.php?s=${searchInputTxt}`)
        .then(response => response.json())
        .then(data => {
            let html = "";
            if (data.meals) {
                data.meals.forEach(meal => {
                    html += `
                        <div class="meal-item" data-id="${meal.idMeal}">
                            <div class="meal-img">
                                <img src="${meal.strMealThumb}" alt="food">
                            </div>
                            <div class="meal-name">
                                <h3>${meal.strMeal}</h3>
                                <a href="#" class="recipe-btn">View Recipe</a>
                            </div>
                        </div>
                        
                    `;
                });
                mealList.classList.remove('notFound');
            } else {
                html = "Sorry, we didn't find any meal!";
                mealList.classList.add('notFound');
            }

            mealList.innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching meal list:', error);
        });
}

// Get recipe of the meal
function getMealRecipe(e) {
    e.preventDefault();
    if (e.target.classList.contains('recipe-btn')) {
        let mealItem = e.target.parentElement.parentElement;
        fetch(`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${mealItem.dataset.id}`)
            .then(response => response.json())
            .then(data => mealRecipeModal(data.meals[0]))
            .catch(error => {
                console.error('Error fetching meal recipe:', error);
            });
    }
}

// Create a modal
function mealRecipeModal(meal) {
    console.log(meal);
    let html = `
        <h2 class="recipe-title" name="name">${meal.strMeal}</h2>
        <p class="recipe-category">Category: ${meal.strCategory}</p>

        <div class="recipe-instruct" name="instructions">
            <h3>Instructions:</h3>
            <p>${meal.strInstructions}</p>
        </div>

        <div class="recipe-meal-img">
            <img src="${meal.strMealThumb}" alt="">
        </div>

        <div class="recipe-link">
            <a href="${meal.strYoutube}" target="_blank">Watch video</a>
        </div>
    `;
    mealDetailsContent.innerHTML = html;
    mealDetailsContent.parentElement.classList.add('showRecipe');
}
function saveRecipe(me) {
    var parent = me.parentElement;
    var name = parent.querySelector(".meal-details-content").querySelector(".recipe-title").textContent;
    var instructions = parent.querySelector(".meal-details-content").querySelector(".recipe-instruct").textContent;


     // Create a hidden form input to store the extracted values
     var nameInput = document.createElement('input');
     nameInput.type = 'hidden';
     nameInput.name = 'name';
     nameInput.value = name;
 
     var instructionsInput = document.createElement('input');
     instructionsInput.type = 'hidden';
     instructionsInput.name = 'instructions';
     instructionsInput.value = instructions;
 
     // Append the hidden inputs to the form
     var form = parent.parentElement
     form.appendChild(nameInput);
     form.appendChild(instructionsInput);

    form.submit()
}


