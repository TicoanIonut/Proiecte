from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

# unregister groups
admin.site.unregister(Group)


# mix profile and user info
class ProfileInline(admin.StackedInline):
	model = Profile


# extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	# display oly username filed
	fields = ['username']
	inlines = [ProfileInline]


# unregister initial User
admin.site.unregister(User)
# reregister User and profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

admin.site.register(Meep)


