
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Amenities, Hotel, HotelBooking)
from django.db.models import Q



    
def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()



    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
    , 'search' : search , 'amenities' : amenities}
    return render(request , 'home.html' ,context)



def hotel_detail(request,uid):
    hotel_obj = Hotel.objects.get(uid = uid)

    if request.method == 'POST':
        # checkin = request.POST.get('checkin')
        # checkout= request.POST.get('checkout')
        hotel = Hotel.objects.get(uid = uid)
        # if not hotel.room_count:
        #     messages.warning(request, 'Ticket not available ')
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date='2023-12-12'
        , end_date = '2023-12-12' , booking_type  = 'Pre Paid')

        hotel.room_count = hotel.room_count - 1
        hotel.save()
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'hotel_detail.html' ,{
        'hotels_obj' :hotel_obj
    })

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        return redirect('/')

        
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'login.html')

def user_logout(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    user_obj = User.objects.filter(username = username)
    logout(request)
    return HttpResponseRedirect('/')



def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'register.html')

def profile_page(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            hotel_name = request.POST.get('event_title')
            hotel_price = request.POST.get('ticket_price')
            description = request.POST.get('description')
            amenities = request.POST.get('event_type')
            room_count = request.POST.get('total_seats')
            print(hotel_name, hotel_price, description, amenities, room_count)
            hotel = Hotel(hotel_name = hotel_name, hotel_price = hotel_price, description = description,  room_count = room_count)
            hotel.amenities.set(amenities)
            hotel.save()
            messages.success(request, 'Event Created successfully !!')
            return HttpResponseRedirect('/home/')

        amenities_objs = Amenities.objects.all()
        return render(request, 'admin_profile_page.html', {'amenities_objs' : amenities_objs})
    elif request.user.is_staff:
        return render(request, 'staff_profile_page.html')
    else:
        User_Bookings = HotelBooking.objects.filter(user = request.user).count()
        print(User_Bookings)
        return render(request, 'user_profile_page.html', {'User_Bookings': User_Bookings})