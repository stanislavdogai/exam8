from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from .models import Product, Review
from .forms import ProductForm, ReviewForm

class ProductIndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/index.html'



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.review.all()
        # reviews = self.object.review.filter(check_moderated=True)
        context['reviews'] = reviews
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('webapp:index')



class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update.html'


class ReviewCreate(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        review = form.save(commit=False)
        review.product = product
        review.author = self.request.user
        review.save()
        return redirect('webapp:product_view', pk=product.pk)

class ReviewDelete(View):
    def get(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        review.delete()
        return redirect('webapp:product_view', review.product.pk)

class ReviewUpdate(UpdateView):
    model = Review
    template_name = 'reviews/update.html'
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):

        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        if review.check_moderated:
            review.check_moderated = False
            review.save()
        return redirect(reverse('webapp:product_view', kwargs={'pk': review.product.pk}))

