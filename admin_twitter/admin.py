from django.contrib import admin
from django.conf import settings
from .models import Tweet
from .models import Author
from .models import Message
from twitter import *
from django.shortcuts import get_object_or_404, render
from django.conf.urls import patterns, url
from django.http import HttpResponse, HttpResponseRedirect
# Register your models here.


def replytweet(modeladmin, request, queryset):
    twitter = Twitter(auth=OAuth(settings.OAUTH_TOKEN, settings.OAUTH_SECRET, settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
    qs = queryset.filter(replied=False)
    for tweet in qs:
        retrievedmessage=Message.objects.filter(active=True).order_by('?').first()

        if retrievedmessage is not None:
            message = "@"+tweet.author+" " + retrievedmessage.message
            print (message)
            try:
                twitter.statuses.update(status=message, in_reply_to_status_id=tweet.id)
                tweet.replied = True
                tweet.save()
            except TwitterHTTPError as api_error:
                print("Error: %s" % (str(api_error)))


replytweet.short_description = "Reply tweet"

def favouritetweet(modeladmin, request, queryset):
    twitter = Twitter(auth=OAuth(settings.OAUTH_TOKEN, settings.OAUTH_SECRET, settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
    qs = queryset.filter(favourited=False)
    for tweet in qs:
        try:
            twitter.favorites.create(_id=tweet.id)
            tweet.favourited = True
            tweet.save()
        except TwitterHTTPError as api_error:
            print("Error: %s" % (str(api_error)))


favouritetweet.short_description = "Favourite tweet"


def followauthor(modeladmin, request, queryset):
    twitter = Twitter(auth=OAuth(settings.OAUTH_TOKEN, settings.OAUTH_SECRET, settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
    qs = queryset.filter(followed=False)
    for author in qs:
        try:
            twitter.friendships.create(screen_name=author.id, follow=False)

            author.followed = True
            author.save()
        except TwitterHTTPError as api_error:
            print("Error: %s" % (str(api_error)))
            

followauthor.short_description = "Follow"



class TweetAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(TweetAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^update/$', self.update)
        )
        return my_urls + urls
    def update(self, request):
        # custom view which should return an HttpResponse
        if request.method == 'GET':
            return render(request, 'admin/updateform.html',)
        else:
            twitter = Twitter(auth=OAuth(settings.OAUTH_TOKEN, settings.OAUTH_SECRET, settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
            result = twitter.search.tweets(q=request.POST.get('search', ''), count=request.POST.get('number', '50'), result_type=request.POST.get('type', 'recent'))

            for tweet in result["statuses"]:
                try:
                    t = Tweet.objects.get(pk=tweet["id"])
                except Tweet.DoesNotExist:
                    t = Tweet()
                    t.id = tweet["id"]
                    t.author = tweet["user"]["screen_name"]
                    t.title = tweet["text"].encode('utf-8')
                    t.search = request.POST.get('search', '')
                    t.save()
                try:
                    a = Author.objects.get(pk=tweet["user"]["screen_name"])
                except Author.DoesNotExist:
                    a = Author()
                    a.id = tweet["user"]["screen_name"]
                    a.save()
            return HttpResponseRedirect("..")
            #return render(request, 'admin/updateform.html',)

    list_display = ['id','date','title','author','replied','favourited','search',]
    ordering = ['-date']
    actions = [replytweet,favouritetweet,]
    list_filter = ('replied', 'favourited')
    search_fields = ['title','author','search',]

    class Media:
        js = ('updatebutton.js', )
    def get_actions(self, request):
        #Disable delete
        actions = super(TweetAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('id','date','title','author',)
        return self.readonly_fields


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','date','followed',]
    list_filter = ('followed',)
    actions = [followauthor,]
    ordering = ['-date']
    search_fields = ['id']
    def get_actions(self, request):
        #Disable delete
        actions = super(AuthorAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class MessageAdmin(admin.ModelAdmin):
    list_display = ['date','message','active',]
    list_filter = ('active',)
    ordering = ['-date']
    search_fields = ['message']

admin.site.register(Tweet, TweetAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Message, MessageAdmin)
