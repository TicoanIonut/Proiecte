from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm


def home(request):
	if request.user.is_authenticated:
		form = MeepForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				meep = form.save(commit=False)
				meep.user = request.user
				meep.save()
				messages.success(request, ('Your Meep has been posted!'))
				return redirect('home')
			
		meeps = Meep.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"meeps": meeps, 'form': form})
	
	else:
		meeps = Meep.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"meeps": meeps})


def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles": profiles})
	else:
		messages.success(request, ('You must be logged in in order to view Profiles'))
		return redirect('home')


def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		meeps = Meep.objects.fileter(user_id=pk).order_by("-created_at")
		if request.method == 'POST':
			current_user_profile = request.user.profile
			action = request.POST['follow']
			if action == 'unfollow':
				current_user_profile.follows.remove(profile)
			elif action == 'follow':
				current_user_profile.follows.add(profile)
			current_user_profile.save()
		return render(request, 'profile.html', {'profile': profile, 'meeps': meeps})
	else:
		messages.success(request, ('You must be logged in in order to view Profiles'))
		return redirect('home')
