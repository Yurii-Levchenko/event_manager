from django.shortcuts import render, redirect

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {"full_name": request.user.full_name(),}
    return render(request, "chat/chat-page.html", context)




# class ChatPageView(View):
#     def get(self, request, meetup_slug):
#         meetup = Meetups.objects.get(slug=meetup_slug)
#         context = {
#             'meetup': meetup,
#         }
#         return render(request, "chat/chat-page.html", context)


# def chatPage(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect("accounts:login")
#     context = {}
#     return render(request, "chat/chat-page.html", context)
