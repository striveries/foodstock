from django.urls import path
from main.views import create_product_flutter, show_main, create_item, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user
from main.views import add_item, reduce_item, delete_item, edit_item, user_page, get_product_json, add_item_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-item', create_item, name='create_item'),   
    path('xml/', show_xml, name='show_xml'), 
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),  
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_item/<int:id>/', add_item, name='add_item'),
    path('reduce_item/<int:id>/', reduce_item, name='reduce_item'),
    path('delete_item/<int:id>/', delete_item, name='delete_item'),
    path('edit-item/<int:id>', edit_item, name='edit_item'),
    path('user-page/', user_page, name='user_page'),
    path('get-product/', get_product_json, name='get_product_json'),
    path('create-ajax/', add_item_ajax, name='add_item_ajax'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
    ]