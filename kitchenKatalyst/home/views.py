from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout #TODO get rid of this
#from django.contrib.auth.forms import UserCreationForm #TODO get rid of this
from .models import User
from .models import Grocery
from .models import Recipe
from .forms import UserForm #form to create new user entry in DB
from .forms import GroceryForm #form to create new grocery entry in DB
from .forms import RecipeForm #form to create new recipe
from .authenticate_user import KKAuthBackend
import re
 
from django.http import HttpResponseRedirect




#whether user logged in or not
loggedIn=False
isAdmin=False
currentUser=None

# Create your views here.
def index(request):

    global loggedIn, isAdmin, currentUser

    if request.method == "POST":
        
        #redirect user to create account view if they clicked create account button
        if "create_account" in request.POST:
            return redirect("create_account")


        #gets elements from webpage (specify in html using name="...")        
        username = request.POST.get('username')
        password = request.POST.get('password')

        auth_backend = KKAuthBackend()
        user = auth_backend.authenticate(request, username=username, password=password)

    

        #normal user
        if user is not None:
        
            login(request, user, backend='home.authenticate_user.KKAuthBackend')
            loggedIn = True
            currentUser = user
            isAdmin = False
            return redirect("main")
        else:

           
            user = authenticate(request, username=username, password=password)

             #admin user
            if user is not None:
                
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                loggedIn = True
                isAdmin = True

                #TODO change this to redirect to home-admin or whatever you want to call it
                return redirect("admin_welcome")

            #return invalid login page
            messages.success(request, ("Invalid email or password")) #FIXME error with message not display
            return redirect("/")   

    else:    
        return render(request, "home/index.html", {})



def create_account(request):

    global loggedIn, currentUser

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():
            
            #TODO fix this logic to return to same page
            if request.POST.get('password') != request.POST.get('password1'):
                return render(request, "home/create_account.html", {'form': form, 'issue': 'passwords_dont_match'})



            # Save user info
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
          

            # Authenticate and login the user using the custom backend
            auth_backend = KKAuthBackend()
            authenticated_user = auth_backend.authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user, backend='home.authenticate_user.KKAuthBackend')
                currentUser = authenticated_user
                loggedIn = True
                return redirect("main")
            else:
                # Handle authentication failure
                return redirect("create_account")
        else:
            # Handle form validation errors
            return render(request, "home/create_account.html", {'form': form, 'issue': 'incomplete'})
    else:
        form = UserForm()
        return render(request, "home/create_account.html", {'form': form, 'issue': None})


#Main.html#
def main(request):

    #don't let user see page if they are not logged in
    if loggedIn == False:
        return redirect("/")

    if loggedIn and isAdmin:
        return redirect("admin_welcome")

  
    # submitted = False
    if request.method == "POST":


        #user wants to add grocery item to DB
        if "add" in request.POST:

        
            form = GroceryForm(request.POST)
            if form.is_valid():
                #set user for form
                form.instance.user = currentUser


                #save grocery item but don't commit to DB yet
                grocery_instance = form.save(commit=False)

                if grocery_instance.unit == 'none':
                    grocery_instance.unit = ''

                grocery_instance.save()
              

                # return HttpResponseRedirect('/main?submitted==True')
            
                #FIXME maybe we don't need this?
                return redirect('main')  # Redirect to the same page after adding item
                
            else:
                messages.error(request, "Invalid form data") #or log invalid entry if they are missing something
           


    else:
        form = GroceryForm() #initialize form

    #query in DB
    grocery_list = Grocery.objects.filter(user=request.user)



    #display all groceries for given user (TODO render them by passing groceries as additional argument)
    return render(request, "home/main.html", {'form': form, 'grocery_list': grocery_list}) 




#ignore this for now
def kitchen(request):
    
    #prevent user from getting access to webpage they shouldn't have access to
    if(loggedIn == False):
        return redirect("/")

    if loggedIn and isAdmin:
        return redirect("admin_welcome")

    #query in DB
    recipe_list = Recipe.objects.filter(user=request.user)

    #display all groceries for given user (TODO render them by passing groceries as additional argument)
    return render(request, "home/kitchen.html", {'recipe_list': recipe_list}) 


def recipe(request):

    #prevent user from getting access to webpage they shouldn't have access to
    if(loggedIn == False):
        return redirect("/")

    if loggedIn and isAdmin:
        return redirect("admin_welcome")


    if request.method == "POST":

        form = RecipeForm(request.POST)

        #TODO don't let user add recipes with duplicate names

         #TODO query DB to check if Recipe for currentUser with form.name already exists
         #if true redirect to "recipe"

        form.instance.user = currentUser
        form.save()


        return render(request, "home/recipe.html", {})
 

       
    else:    
        #display all groceries for given user (TODO render them by passing groceries as additional argument)
        form=RecipeForm()
        return render(request, "home/recipe.html", {}) 





def admin_welcome(request): 

    if loggedIn == False:
        return redirect("/") #if user not logged in, don't let them see page

    if loggedIn and isAdmin == False:
        return redirect("/main") #if user is not admin, redirect them to their account page

    return render(request, "home/admin_welcome.html") #f user is admin, show admin page
  

#signs user out of their account
def logout(request):

    global loggedIn, isAdmin, currentUser

    #if user is logged in, don't let them trigger this view
    if loggedIn == False:
        return redirect("/") 
    

    #user is logged in
    else:

        #reset session info
        loggedIn=False
        isAdmin=False
        currentUser=None
        logout(request)

        #take them back to login page
        return redirect("/")


#deletes grocery with given grocery_number from DB and redirects user to homepage
def delete(request, grocery_number):


    if loggedIn == False:
        return redirect("/") #if user not logged in, don't let them see page

    if loggedIn and isAdmin:
        return redirect("admin_welcome") #if user is admin, don't let them see this page


    try:
        #query DB for grocery to delete
        grocery=get_object_or_404(Grocery, groceryID=grocery_number)

        #try to delete grocery
        grocery.delete()

        #return user to main page
        return redirect('main')

    except Http404:

        #TODO Gerson make simple custom web page and render it
        return HttpResponse("404 page not found!")
    

#TODO
# add view for admin-home or whatever that renders an html webpage
    #if isAdmin 
        #render page they should see
    #else 
        #redirect("main")


#TODO maybe do UberEats/instacart view
    #verify user is logged in
    #display webpage
    #I think that's it?
