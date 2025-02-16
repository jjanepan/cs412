"""
views.py

View functions for the restaurant application.

Author: Jane Pan
Date: February 14, 2025
"""
import random
from datetime import datetime, timedelta
from django.shortcuts import render

def main(request):
    # Main page: restaurant info
    context = {
        'name': 'Burger Haven',
        'location': '123 Burger Blvd, Boston, MA',
        'hours': [
            'Monday - Friday: 11 AM - 11 PM',
            'Saturday - Sunday: 12 PM - Midnight'
        ],
        'photo': 'restaurant/burger_home.jpg',  # Path to photo in static files
    }
    return render(request, 'restaurant/main.html', context)

def order(request):
    # Order page: display order form, including a daily special
    daily_specials = [
        {'name': 'Cheesy Bacon Burger', 'price': 12.99},
        {'name': 'Veggie Burger', 'price': 10.99},
        {'name': 'Double Stack Burger', 'price': 14.99},
        {'name': 'Spicy Chicken Burger', 'price': 11.99},
    ]
    daily_special = random.choice(daily_specials)
    context = {
        'daily_special': daily_special,
        # List your regular menu items (example):
        'menu_items': [
            {'name': 'Classic Burger', 'price': 9.99},
            {'name': 'Fries', 'price': 3.99},
            {'name': 'Onion Rings', 'price': 4.99},
            {'name': 'Soda', 'price': 1.99},
        ]
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    # Confirmation page: process form data, calculate total price, and ready time.
    if request.method == 'POST':
        selected_items = []
        total_price = 0.0

        # Regular menu items and prices:
        menu_prices = {
            'Classic Burger': 9.99,
            'Fries': 3.99,
            'Onion Rings': 4.99,
            'Soda': 1.99,
        }
        # Check which items were ordered:
        for item, price in menu_prices.items():
            if request.POST.get(item):  # checkbox is checked
                selected_items.append({'name': item, 'price': price})
                total_price += price

        # Daily Special:
        if request.POST.get(request.POST.get('daily_special_name')):
            # In this simple example, if the daily special checkbox is checked:
            daily_special_price = float(request.POST.get('daily_special_price', 0))
            selected_items.append({
                'name': request.POST.get('daily_special_name'),
                'price': daily_special_price
            })
            total_price += daily_special_price

        # Collect customer info:
        customer_info = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'instructions': request.POST.get('instructions'),
        }

        # Calculate a random ready time between 30 and 60 minutes from now:
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
        context = {
            'selected_items': selected_items,
            'total_price': round(total_price, 2),
            'ready_time': ready_time.strftime("%I:%M %p"),
            'customer_info': customer_info,
        }
        return render(request, 'restaurant/confirmation.html', context)
    else:
        return render(request, 'restaurant/order.html')
