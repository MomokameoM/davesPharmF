"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drug_store import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.signin, name="signin"),
    path("products/", views.get_products, name="products"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/generic/true", views.get_products_generics, name="products_generic"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),
    path("products/prescription/true/", views.products_required_prescription, name="products_prescription"),
    path("products/prescription/false/", views.products_no_prescription, name="products_no_prescription"),
    path("remission_note/create/", views.create_remission_note, name="create_remition_note"),
    path("remission_note/details/<int:remission_note_id>/", views.remission_note_edit, name="remission_note_details"),
    path("remission_notes/", views.get_remission_notes, name="remission_notes"),
    path("provideers/", views.get_provideers, name="provideers"),
    path("bills/", views.get_bill, name="bill"),
    path("bill/create", views.create_bill, name="create_bill"),
    path("bill/edit", views.edit_bill, name="edit_bill"),
    path("clients/", views.get_clients, name="clients"),
    path("clients/create/", views.create_client, name="create_client"),
    path("clients/edit/<int:client_id>/", views.edit_client, name="edit_client"),
    path("clients/delete/<int:client_id>/", views.delete_client, name="delete_client"),
    path("sale_details/", views.get_sale_details, name="sale_details"),
    path("sale_details/create/", views.create_sale_details, name="create_sale_details"),
    
]
