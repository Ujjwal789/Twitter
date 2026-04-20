from django.shortcuts import render

# Create your views here.
def post_tweet(request):
    return render(request, 'post_tweet.html')