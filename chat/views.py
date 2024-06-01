from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Message
from account.models import CustomUser


@login_required
def message(request, id):
    user = CustomUser.objects.get(id=id)
    admin = CustomUser.objects.get(username='ahmat')
    text = request.POST.get('message')
    if request.user.username == 'ahmat':
        message, created = Message.objects.get_or_create(user=admin,
                                                         user_to=user,
                                                         text=text)
        return redirect('chat:chat_detail', user.id)
    message, created = Message.objects.get_or_create(user=user,
                                                     user_to=admin,
                                                     text=text)
    message.save()
    return redirect('shop:contacts')


def chat_list(request):
    messages = Message.objects.exclude(user__username='ahmat')
    return render(request,
                  'chat/chat.html',
                  {'messages': messages})


def chat_detail(request, id):
    message = Message.objects.get(id=id)
    user = message.user
    messages_user = Message.objects.filter(user__id=user.id)
    admin = CustomUser.objects.get(username='ahmat')
    messages_admin = Message.objects.filter(user=admin, user_to=user)
    messages = []
    l_user = [i for i in messages_user]
    l_admin = [i for i in messages_admin]
    print(l_user, l_admin)
    while l_user and l_admin:
        if l_user[0].date < l_admin[0].date:
            messages.append(l_user[0])
            del l_user[0]
        elif l_user[0].date == l_admin[0].date:
            if l_user[0].time < l_admin[0].time:
                messages.append(l_user[0])
                del l_user[0]
            else:
                messages.append(l_admin[0])
                del l_admin[0]
        else:
            messages.append(l_admin[0])
            del l_admin[0]
    messages.extend(l_user)
    messages.extend(l_admin)
    return render(request,
                  'chat/chat_detail.html',
                  {'message': message,
                   'messages': messages})
