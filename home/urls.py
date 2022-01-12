from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.home,name='home'),
    path('quick_search/<rma>/<sn>/',views.quick_search,name='quick-search'),
    path('update/<rma_id>/',views.update_pending,name='update-pending'),
    path('partsorder/<serial>/',views.parts_order,name='parts-order'),
    path('comments/<rma_id>/',views.comments,name='comments'),
    path('devices_xls/',views.devices_xls,name='devices-xls'),

    

]