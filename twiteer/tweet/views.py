from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = User.objects.first() 
            t.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    tweets = tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet/post_tweet.html', {'form': form, 'tweets': tweets})

def tweet_list(request):
    tweets = tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet/tweet_list.html', {'tweets': tweets})

@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.user = request.user
            new_tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet/tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet_instance = get_object_or_404(tweet, pk=tweet_id) 
    if tweet_instance.user != request.user:   # ✅ ownership check
        return HttpResponseForbidden("You can't edit someone else's tweet.")
     
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet_instance)
        if form.is_valid():
            updated_tweet = form.save(commit=False)
            updated_tweet.user = request.user 
            updated_tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet_instance)
    return render(request, 'tweet/tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet_instance = get_object_or_404(tweet, pk=tweet_id)  
    if tweet_instance.user != request.user:   # ✅ ownership check
        return HttpResponseForbidden("You can't delete someone else's tweet.")
    
    if request.method == 'POST':
        tweet_instance.delete()
        return redirect('tweet_list')
    return render(request, 'tweet/tweet_delete.html', {'tweet': tweet_instance}) 

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()          # handles password hashing automatically
            login(request, user)
            return redirect('tweet_list')
        # if form invalid, fall through and re-render with errors
    else:
        form = UserRegistrationForm()   # ✅ only create blank form on GET
    
    return render(request, 'registration/register.html', {'form': form})  # ✅ pass instance