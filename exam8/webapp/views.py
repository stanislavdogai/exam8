from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from .models import Product, Review
from .forms import ProductForm, ReviewForm, ReviewCheckForm


class ProductIndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/index.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    permission_required = 'webapp.add_product'

    def get_product_form(self):
        form_kwargs = {'instance' : self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProductForm(**form_kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.review.all()
        context['reviews'] = reviews
        return context


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update.html'
    permission_required = 'webapp.change_product'

    def get_product_form(self):
        form_kwargs = {'instance' : self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProductForm(**form_kwargs)


class ReviewCreate(LoginRequiredMixin, CreateView):
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


class ReviewDelete(PermissionRequiredMixin, View):
    permission_required = 'webapp.delete_review'

    def get(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        review.delete()
        return redirect('webapp:product_view', review.product.pk)


class ReviewUpdate(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'reviews/update.html'
    form_class = ReviewForm
    permission_required = 'webapp.change_review'

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        if review.check_moderated:
            review.check_moderated = False
            review.save()
        return redirect(reverse('webapp:product_view', kwargs={'pk': review.product.pk}))

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()


class ReviewNotModeratedView(ListView):
    model = Review
    template_name = 'reviews/not_moderated.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(check_moderated=False)
        return context


class CheckReview(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'reviews/update.html'
    form_class = ReviewCheckForm
    permission_required = 'webapp.can_view_not_moderated_list'