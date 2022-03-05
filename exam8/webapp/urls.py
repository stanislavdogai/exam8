from django.urls import path

from .views import ProductIndexView, ProductCreateView, ProductDeleteView, \
    ProductDetailView, ProductUpdateView, ReviewCreate, ReviewUpdate, ReviewDelete

app_name = 'webapp'

urlpatterns = [
    path('', ProductIndexView.as_view(), name='index'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/review/create/', ReviewCreate.as_view(), name='review_create'),
    path('review/<int:pk>/update/', ReviewUpdate.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDelete.as_view(), name='review_delete'),
]