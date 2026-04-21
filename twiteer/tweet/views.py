from django.shortcuts import get_object_or_404, render, redirect
from .models import tweet
from .forms import TweetForm
from django.contrib.auth.models import User

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

def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.user = User.objects.first()  
            new_tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet/tweet_form.html', {'form': form})

def tweet_edit(request, tweet_id):
    tweet_instance = get_object_or_404(tweet, pk=tweet_id)  
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet_instance)
        if form.is_valid():
            updated_tweet = form.save(commit=False)
            updated_tweet.user = User.objects.first()  
            updated_tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet_instance)
    return render(request, 'tweet/tweet_form.html', {'form': form})

def tweet_delete(request, tweet_id):
    tweet_instance = get_object_or_404(tweet, pk=tweet_id)  
    if request.method == 'POST':
        tweet_instance.delete()
        return redirect('tweet_list')
    return render(request, 'tweet/tweet_delete.html', {'tweet': tweet_instance}) 