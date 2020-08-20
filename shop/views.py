import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from rest_framework import generics

from .forms import CheckoutForm, CreateUserForm, SignUpForm
from .models import *
from .serializers import CartItemsSerializer, QuickViewSerializer

# Defined a global dictionary for sets of items
we = "সমীকরণ.কম"
page_titles = {
    "category-page"    : we,
    "sub-category-page": we,
    "login-page"       : we + " ~ Log In",
    "about-page"       : we + " - About Us",
    "contact-page"     : we + " - Contact",
    "cattle-page"      : we + " ~ Online Gorur Haat 2020",
    "item-page"        : we + " ~ Buy Products at cheapest price"
}
DEMO = "REPLACE"


def user_login(request):
    # return render(request, 'shop/custom_login.html')
    if request.user.is_authenticated:
        return redirect('shop:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('Phone')
            password = request.POST.get('Password')
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('shop:home')
                else:
                    messages.info(request, 'Username OR password is incorrect')

            else:
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user, created = User.objects.get_or_create(username=username)
                    user.set_password(password)
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, 'Account was created for ' + username)
                    return redirect('shop:home')
                else:
                    messages.success(request, 'Please enter correctly ')
        form = SignUpForm()
        context = {
            'form'      : form,
            'page_title': page_titles["login-page"]}
        return render(request, 'shop/custom_login.html', context)


class HomeView(ListView):
    template_name = 'shop/index.html'
    paginate_by = 8
    model = Items

    def get_context_data(self, **kwargs):
        try:
            cartitems = Order.objects.get(user=self.request.user, ordered=False)
        except:
            cartitems = ''
        context = super().get_context_data(**kwargs)
        context['somikoron_items'] = Items.objects.filter(
            itemdetails__stock_quantity__gt=0,
            sub_category__category__category_id='somikoron')
        context['popular'] = Items.objects.filter(itemdetails__stock_quantity__gt=0).order_by(
            '-itemdetails__total_views')
        context['offer'] = Items.objects.filter(itemdetails__stock_quantity__gt=0).order_by(
            '-itemdetails__discount_offer')
        context['all_items'] = Items.objects.filter(itemdetails__stock_quantity__gt=0)
        context['categories'] = get_categories()
        context['cartitems'] = cartitems
        return context


def get_categories():
    return Category.objects.all()


def get_subcategories():
    return SubCategory.objects.all()


class ItemListView(View):
    def get(self, *args, **kwargs):
        item_list = Items.objects.filter(sub_category_id=kwargs['subid'],
                                         itemdetails__stock_quantity__gt=0)
        page = self.request.GET.get('page', 1)

        paginator = Paginator(item_list, 18)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        cat = Category.objects.get(subcategory=kwargs['subid'])
        context = {
            'items'        : items,
            'categories'   : get_categories(),
            'item_category': cat,
            'page_title'   : page_titles["sub-category-page"] + " - " + cat.category_name,
        }
        return render(self.request, 'shop/shop_item_list.html', context)


class CategoryItemView(View):
    def get(self, *args, **kwargs):
        cat = Category.objects.get(category_id=kwargs['catid'])
        item_list = Items.objects.filter(sub_category__category=cat,
                                         itemdetails__stock_quantity__gt=0)
        page = self.request.GET.get('page', 1)

        paginator = Paginator(item_list, 21)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context = {
            'items'        : items,
            'categories'   : get_categories(),
            'item_category': cat,
            'page_title'   : page_titles["category-page"] + " - " + cat.category_name,
        }
        return render(self.request, 'shop/shop_item_list.html', context)


class ItemDetailsView(DetailView):
    template_name = 'shop/shop_detail.html'
    model = ItemDetails

    def get_context_data(self, **kwargs):
        context = super(ItemDetailsView, self).get_context_data(**kwargs)
        context['categories'] = get_categories()
        context['page_title'] = page_titles["item-page"] + DEMO
        # item = Items.objects.get(pk='GR02')
        # context['images'] = ItemImages.objects.all()
        return context


@login_required(login_url="/user_login")
def add_to_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This item quantity was updated.")
            # return redirect("shop:itemdetails", slug=slug)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            order.items.add(order_item)
            messages.success(request, "This item was added to your cart.")
            # return redirect("shop:itemdetails", slug=slug)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item was added to your cart.")
        # return redirect("shop:itemdetails", slug=slug)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/user_login/")
def remove_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.error(request, "This item was removed from your cart.")
            # return redirect("shop:itemdetails", slug=slug)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "This item was not in your cart")
            # return redirect("shop:itemdetails", slug=slug)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "You do not have an active order")
        # return redirect("shop:itemdetails", slug=slug)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/user_login/")
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:home", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:home", slug=slug)


def add_to_cart_demo(request):
    return render(request, 'shop/add-to-cart-demo.html')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object'    : order,
                'categories': get_categories()
            }
            return render(self.request, 'shop/shop_cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


# Demo
@csrf_exempt
def get_cart_items(request):
    print(Order.objects.get(user=request.user, ordered=False))
    items = Order.objects.get(user=request.user, ordered=False)
    data = serializers.serialize('json', [items.items])
    # data = serializers.serialize('json', cart)
    print(data)
    return HttpResponse(data, safe=False)


# endDemo

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            address = Address.objects.get(user=self.request.user)
        except:
            address = ''
        form = CheckoutForm()
        try:
            orders = Order.objects.filter(user=self.request.user, ordered=False)
            order = orders[0]
        except:
            order = ''
        context = {
            'form'      : form,
            'object'    : order,
            'address'   : address,
            'categories': get_categories()
        }
        return render(self.request, 'shop/shop_checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                customer_name = form.cleaned_data.get('customer_name')
                customer_phone = form.cleaned_data.get('customer_phone')
                area = form.cleaned_data.get('area')
                address = form.cleaned_data.get('address')
                order_notes = form.cleaned_data.get('order_notes')
                # payment_method = form.cleaned_data.get('payment_option')
                # print(payment_option)
                if Address.objects.filter(user=self.request.user):
                    shipping_address = Address.objects.get(user=self.request.user)
                    shipping_address.customer_name = customer_name
                    shipping_address.customer_phone = customer_phone
                    shipping_address.area = area
                    shipping_address.address = address
                    # shipping_address.payment_method = payment_method
                    shipping_address.save()
                else:
                    shipping_address = Address(
                        user=self.request.user,
                        customer_name=customer_name,
                        customer_phone=customer_phone,
                        area=area,
                        address=address,
                        # payment_method=payment_method,
                    )
                    shipping_address.save()

                shipping_address = Address.objects.get(user=self.request.user)
                order.shipping_address = shipping_address
                order.order_note = order_notes
                order.ordered = True
                order.save()
                # messages.success(self.request, "Order placed successfully")
                context = {
                    'object' : order,
                    'address': shipping_address
                }
                return render(self.request, 'shop/shop_order_complete.html', context)
            messages.success(self.request, "Failed! Form is invalid")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('shop:order-summary')


class OrderCompleteView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'shop/shop_order_complete.html')


class CattleshopView(View):

    def get(self, *args, **kwargs):
        sub_category = SubCategory.objects.filter(category__category_id='cattle')
        cattle_list = Items.objects.filter(sub_category__category__category_id='cattle', itemdetails__stock_quantity__gt=0)

        page = self.request.GET.get('page', 1)

        paginator = Paginator(cattle_list, 27)
        try:
            cattles = paginator.page(page)
        except PageNotAnInteger:
            cattles = paginator.page(1)
        except EmptyPage:
            cattles = paginator.page(paginator.num_pages)

        print(cattles)
        context = {
            'cattles'   : cattles,
            'categories': get_categories(),
            'page_title': page_titles["cattle-page"]
        }
        return render(self.request, 'shop/special_offer.html', context)


class QuickView(generics.ListAPIView):
    # def get(self, *args, **kwargs):
    # instance = get_object_or_404(Items, slug='cow1')
    # context = {
    #     'instance': instance
    # }
    # print(instance)
    # return render(self.request, 'shop/quick_view.html', context)

    serializer_class = QuickViewSerializer
    print(serializer_class)

    def post(self, *args, **kwargs):
        queryset = Items.objects.get(slug=kwargs['slug'])
        # data = serializers.serialize('json', [queryset])
        serializer = QuickViewSerializer(queryset)
        return JsonResponse(serializer.data, safe=False, )


def quickview(request):
    result = {'html': render_to_string('your-template.html', {})}
    return HttpResponse(json.dumps(result, ensure_ascii=False),
                        content_type='application/json')


class CartItemView(generics.ListAPIView):
    serializer_class = CartItemsSerializer
    print(serializer_class)

    def post(self, *args, **kwargs):
        queryset = Order.objects.get(user=self.request.user, ordered=False)
        # data = serializers.serialize('json', [queryset])
        serializer = CartItemsSerializer(queryset)
        return JsonResponse(serializer.data, safe=False, )


# demo
def cart_demo(request):
    return render(request, 'shop/cart_demo.html')


def about_us(request):
    return render(request, 'shop/about_us.html', {
        'categories': get_categories(),
        'page_title': page_titles["about-page"]})


def contact_us(request):
    return render(request, 'shop/contact.html', {
        'categories': get_categories(),
        'page_title': page_titles["contact-page"]})


@csrf_exempt
def plcae_order(request):
    # for a in request.POST.getlist('carts[]'):
    # print(json.loads(request.POST.get('carts')))
    # cartitems = json.loads(request.POST.get('cart'))
    if not request.user.is_authenticated:
        return HttpResponse('false')
    else:
        cart_items = request.POST['carts']
        data = json.loads(cart_items)
        print(data[0]['name'])
        # print(cartitems)
        for cart_item in data:
            print(cart_item['name'])
            print(cart_item['quantity'])
            item = get_object_or_404(Items, product_code=cart_item['name'])
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False,
            )
            order_item.quantity = cart_item['quantity']
            order_item.save()
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order

                order.items.add(order_item)
                messages.success(request, "This item was added to your cart.")
                # return redirect("shop:itemdetails", slug=slug)
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(
                    user=request.user, ordered_date=ordered_date)
                order.items.add(order_item)
                messages.success(request, "This item was added to your cart.")
                # return redirect("shop:itemdetails", slug=slug)
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('true')


def delivery_status(request):
    order = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    context = {
        'categories': get_categories(),
        'orders'    : order,
    }
    return render(request, 'shop/delivery_status.html', context)


def monthly_shopping(request):
    return render(request, 'monthly_order/monthly_market.html')


def place_monthly_order(request):
    if request.method == 'POST':
        phone = request.POST['c_phone']
        name = request.POST['c_name']
        area = request.POST['c_area']
        full_address = request.POST['c_address']
        order_list = request.POST['order_list']
        payment_method = request.POST['m_payment']

        # create user account if does not exist
        if not request.user.is_authenticated:
            if not User.objects.filter(username=phone).exists():
                user, created = User.objects.get_or_create(username=phone)
                user.set_password("somikoron")
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'An account has been created for ' + phone + '\nusername: ' + phone + ' and password: somikoron')

        address, created = Address.objects.get_or_create(user = request.user)
        address.area = area
        address.customer_name = name
        address.customer_phone = phone
        address.address = full_address
        address.save()

        monthly_order = MonthlyPackage.objects.create(user = request.user, shipping_address=address, order_list=order_list,payment_method=payment_method)
        monthly_order.save()
        messages.success(request, 'Your order has been placed. We will confirm your order soon.')
        return redirect(f'/monthly_order_invoice/{monthly_order.pk}')
    messages.success(request, 'Failed to place your order')
    return redirect('shop:home')

@login_required
def monthly_order_invoice(request, orderid):
    order = MonthlyPackage.objects.get(id = orderid)
    address = Address.objects.get(user_id=order.user_id)
    context = {
        'address': address,
        'object': order,
    }
    return render(request, 'monthly_order/order_invoice.html',context)




