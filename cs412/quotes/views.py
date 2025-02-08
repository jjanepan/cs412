from django.shortcuts import render
import random

# Quotes and images list
QUOTES = [
    "Let go of the things that make you feel dead! Life is worth living!",
    "When a door closes, you have two choices: give up, or keep going.",
    "Success is not about the end result, it’s about what you learn along the way.",
    "It’s tougher to be vulnerable than to actually be tough.",
    "I always believed that when you follow your heart, it eventually leads you to the right place."
]

IMAGES = [
    "quotes/rihanna1.png",
    "quotes/rihanna2.png",
    "quotes/rihanna3.png",
    "quotes/rihanna4.png",
    "quotes/rihanna5.png"
]

def quote(request):
    """Displays a single random quote and image"""
    context = {
        'quote': random.choice(QUOTES),
        'image': random.choice(IMAGES),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    """Displays all quotes and images"""
    context = {
        'quotes': QUOTES,
        'images': IMAGES,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    """Displays the About page"""
    return render(request, 'quotes/about.html')
