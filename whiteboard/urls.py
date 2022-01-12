from django.urls import path
from . import views



urlpatterns = [
    
    path('events/',views.events,name='events'),
    path('',views.feed_back,name='feed-back'),
    path('verified_comment/<comment_id>',views.verify_comment,name='verify-comment'),
    path('new_members/',views.new_members,name='new-members'),
    path('update_member/<member_id>',views.update_member,name='update-member'),
    path('update_event/<event_id>',views.update_event,name='update-event'),
    path('add_event/',views.add_event,name='add-event'),
    path('tong_hop/',views.tong_hop,name='tong-hop'),
    path('quote_info/',views.quote_info,name='quote-info'),
    


    

    

]