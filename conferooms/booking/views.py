import datetime
from django.shortcuts import render, redirect
from django.views import View
from booking.models import Room, Reservation


class AddRoom(View):
    def get(self, request):
        return render(request, "main.html", context={"middle": "add_room.html"})

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = bool(request.POST.get("projector"))
        error = ""
        if name == "":
            error = "Please enter room name"
            return render(request, "main.html", context={"middle": "add_room.html", "error": error})
        if Room.objects.filter(name=name).exists():
            error = "Name already taken"
            return render(request, "main.html", context={"middle": "add_room.html", "error": error})
        if capacity == "" or int(capacity) <= 0:
            error = "Invalid capacity"
            return render(request, "main.html", context={"middle": "add_room.html", "error": error})
        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect("/")


class AllRooms(View):
    def get(self, request):
        rooms = Room.objects.all().order_by("name")
        today = datetime.date.today()
        for room in rooms:
            is_reserved = room.reservation_set.filter(date=today).exists()
            room.is_reserved = is_reserved
        return render(request, "main.html", context={"rooms": rooms, "middle": "all_rooms.html"})


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect("/")


class ModifyRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request, "main.html", context={"room": room, "middle": "modify_room.html"})

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = bool(request.POST.get("projector"))
        error = ""
        if name == "":
            error = "Please enter room name"
            return render(request, "main.html", context={"room": room, "middle": "modify_room.html", "error": error})
        if name != room.name:
            if Room.objects.filter(name=name).exists():
                error = "Name already taken"
                return render(request, "main.html", context={"room": room, "middle": "modify_room.html", "error": error})
        if capacity == "" or int(capacity) <= 0:
            error = "Invalid capacity"
            return render(request, "main.html", context={"room": room, "middle": "modify_room.html", "error": error})
        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()
        return redirect("/")


class ReserveRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        name = room.name
        reservations = room.reservation_set.filter(date__gte=datetime.date.today()).order_by("date")
        return render(request, "main.html", context={"name": name, "middle": "reserve_room.html", "reservations": reservations})

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        comment = request.POST.get("comment")
        date = request.POST.get("date")
        if not date:
            ctx ={
                "name": room.name,
                "middle": "reserve_room.html",
                "error": "Please select a date",
                "comment": comment
            }
            return render(request, "main.html", context=ctx)
        if room.reservation_set.filter(date=date).exists():
            ctx ={
                "name": room.name,
                "middle": "reserve_room.html",
                "error": "Room already reserved",
                "comment": comment
            }
            return render(request, "main.html", context=ctx)
        if date < str(datetime.date.today()):
            ctx ={
                "name": room.name,
                "middle": "reserve_room.html",
                "error": "Date already expired",
                "comment": comment
            }
            return render(request, "main.html", context=ctx)
        Reservation.objects.create(comment=comment, date=date, room=room)
        return redirect("/")


class RoomDetails(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        reservations = room.reservation_set.filter(date__gte=datetime.date.today()).order_by("date")
        ctx = {
            "middle": "room_details.html",
            "room": room,
            "reservations": reservations
        }
        return render(request, "main.html", context=ctx)


class SearchEngine(View):
    def get(self, request):
        name = request.GET.get("name")
        capacity = request.GET.get("capacity")
        projector = bool(request.GET.get("projector"))
        rooms = Room.objects.all()
        if name:
            rooms = rooms.filter(name__icontains=name)
        if capacity:
            rooms = rooms.filter(capacity__gte=int(capacity))
        if projector:
            rooms = rooms.filter(projector=True)
        today = datetime.date.today()
        for room in rooms:
            is_reserved = room.reservation_set.filter(date=today).exists()
            room.is_reserved = is_reserved
        return render(request, "main.html", context={"rooms": rooms, "middle": "all_rooms.html"})