from django.shortcuts import render

# Create your views here.

def meetups_page(request):
    meetups = [
        {"title": "Chess Tournament",
         'location': 'Kyiv',
         'slug': 'first-meetup'},
        {"title": 'Push up Challange',
         'location': 'Lviv',
         'slug': 'second-meetup'},
    ]

    return render(request, 'meetups/meetups_page.html', {
        'show_meetups': True,
        'meetups': meetups
    })

def meetup_details(request, meetup_slug):
    print(meetup_slug)
    selected_meetup = {
        'title': 'A first meetup',
        'description': 'This is '
    }
    return render(request, 'meetups/meetup_details.html', {
        'meetup_title': selected_meetup['title'],
        'meetup_description': selected_meetup['description'],
    })