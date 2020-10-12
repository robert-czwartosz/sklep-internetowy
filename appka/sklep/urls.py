from django.urls import path

from . import views

app_name = 'sklep'

urlpatterns = [
    ### USER ###
    # ex: /sklep/signup/
    path('signup/', views.signup, name='signup'),
    # ex: /sklep/login/
    path('login/', views.login, name='login'),
    # ex: /sklep/auth/
    path('auth/', views.auth, name='auth'),
    # ex: /sklep/loggedin/
    path('loggedin/', views.loggedin, name='loggedin'),
    # ex: /sklep/loggedout/
    path('loggedout/', views.loggedout, name='loggedout'),

    # ex: /sklep/listprod/12/
    path('listprod/<int:user_id>/', views.listProdUser, name='listprodUser'),

    # ex: /sklep/findord/12/
    path('findord/<int:user_id>/', views.findOrderUser, name='findordUser'),
    # ex: /sklep/findord/12/delete/2/
    path('findord/<int:user_id>/delete/<int:order_id>/', views.deleteOrderUser, name='delete_orderUser'),
    # ex: /sklep/order/12/2/
    path('order/<int:user_id>/<int:prod_id>/', views.orderProdUser, name='orderProdUser'),
    

    ### ADMIN #####
    # ex: /sklep/addemp/
    path('addemp/', views.addEmp, name='addemp'),
    # ex: /sklep/emp/edit/11/
    path('emp/edit/<int:emp_id>/', views.editEmp, name='edit_emp'),
    # ex: /sklep/emp/delete/33/
    path('emp/delete/<int:emp_id>/', views.deleteEmp, name='delete_emp'),
    # ex: /sklep/listemp/
    path('listemp/', views.listEmp, name='listemp'),

    # ex: /sklep/addproduct/
    path('addproduct/', views.addProduct, name='addproduct'),
    # ex: /sklep/prod/edit/11/
    path('prod/edit/<int:prod_id>/', views.editProd, name='edit_prod'),
    # ex: /sklep/listprod/
    path('listprod/', views.listProd, name='listprod'),

    # ex: /sklep/findusr/
    path('findusr/', views.findUser, name='findusr'),
    # ex: /sklep/findusr/delete/9/
    path('findusr/delete/<int:user_id>/', views.deleteUser, name='delete_user'),
    # ex: /sklep/findusr/edit/9/
    path('findusr/edit/<int:user_id>/', views.editUser, name='edit_user'),

    # ex: /sklep/findord/
    path('findord/', views.findOrder, name='findord'),
    # ex: /sklep/findord/delete/2/23
    path('findord/delete/<int:order_id>/<int:user_id>', views.deleteOrder, name='delete_order'),
	# ex: /sklep/findord/orderSetStatus/2/
    path('findord/orderSetStatus/<int:order_id>', views.orderSetStatus, name='orderSetStatus'),
]
