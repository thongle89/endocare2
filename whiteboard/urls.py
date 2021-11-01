from django.urls import path
from . import views



urlpatterns = [
    
    path('events',views.events,name='events'),
    path('',views.feed_back,name='feed-back'),
    path('verified_comment/<comment_id>',views.verify_comment,name='verify-comment')
    

    

]