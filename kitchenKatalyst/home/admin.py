from django.contrib import admin
from .models import User, Security_Question, Password_History, Grocery, Recipe

# Register your models here.
admin.site.register(User)
admin.site.register(Security_Question)
admin.site.register(Password_History)
admin.site.register(Grocery)
admin.site.register(Recipe)
