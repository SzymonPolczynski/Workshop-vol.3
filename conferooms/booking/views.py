from django.shortcuts import render, redirect
from django.views import View

from booking.models import Room


class AddRoom(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = bool(request.POST.get("projector"))
        error = ""
        if name == "":
            error = "Please enter room name"
            return render(request, "add_room.html", context={"error": error})
        if Room.objects.filter(name=name).exists():
            error = "Name already taken"
            return render(request, "add_room.html", context={"error": error})
        if capacity == "" or int(capacity) < 0:
            error = "Invalid capacity"
            return render(request, "add_room.html", context={"error": error})
        room = Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect("/")


class AllRooms(View):
    def get(self, request):
        rooms = Room.objects.all().order_by("-name")
        return render(request, "main.html", context={"rooms": rooms})


def delete_room(request, room_id):
