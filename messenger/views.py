from django.shortcuts import render, redirect
from messenger.models import Room, Message
from django.http import HttpResponse, JsonResponse
# Create your views here.
def home(request):
    return render(request,'home.html');

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    # first we access the room_name and the username when submit button is clicked.
    # we use POST because that is the method that was used to submit the list
    room = request.POST['room_name']
    username = request.POST['username']

    # here we check if the room already exists in our database and if it does we redirect the user to where it is
    # that part for room and username is displayed above our page
    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
        # if the room doesn't exist the system creates a new room and saves it in our database and then redirects the user to the newly created room
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


# this function handles the new messages being written
# you can see it first gets the message, username and room_id but uses POST because it's the method used to send the form
#  so when send is clicked the message is created and saved in the database
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

# this is the function that the system uses to continuously access the data in a page and updating it and still showing the messages for that particular group
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
