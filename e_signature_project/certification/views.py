from django.shortcuts import render, redirect
from .models import RegisteredUser
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        public_key_file = request.FILES['public_key']

        try:
            public_key = public_key_file.read().decode('utf-8')
            RegisteredUser.objects.create(username=username, public_key=public_key)
            messages.success(request, "Utilisateur enregistré avec succès !")
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

        # ici, on retourne la page, indentation alignée avec if
        return render(request, 'certification/register.html')

    # sinon, on affiche la page normalement
    return render(request, 'certification/register.html')


def get_registered_user(request):
    if request.method == 'GET':
        users = RegisteredUser.objects.all()
        return render(request, 'certification/user_list.html', {'users': users})
