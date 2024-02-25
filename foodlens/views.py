from django.shortcuts import render,redirect
from .mingo import prediction
from .forms import ImageForm,IntakeForm
from userprofile.models import UserProfile
from .models import Nutrients,Intake
from django.http import JsonResponse

# Create your views here.



def foodlensFunction(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = ImageForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        img_obj = form.instance
            
        return render(request,'foodlens.html',{'form':form,'img_obj':img_obj})
    else:
        form = ImageForm()
        return render(request,'foodlens.html', {'form': form,'user_profile':user_profile})


def foodlensresultFunction(request):
    global TOTAL_NUTRIENTS_TODAY
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            predicted_food = prediction(img_obj.image.path)
            calories = get_calories_for_food(predicted_food)
            # print(TOTAL_NUTRIENTS_TODAY)
            return render(request, 'foodlensresult.html', {'predicted_food': predicted_food, 'calories': calories,'img_obj':img_obj,'user_profile': user_profile})
            print(calories)
    else:
        form = ImageForm()
    return render(request, 'foodlens.html', {'form': form})

def get_calories_for_food(food_name):
    nutrients = Nutrients.objects.filter(food=food_name).first()   
    if nutrients:
        return nutrients.energy  # Assuming 'energy' field represents calories
    return None

# def get_calories_for_food(request):
#     calories_data = Intake.objects.filter(user=request.user).values_list('timestamp', 'calories')
#     return JsonResponse(list(calories_data), safe=False)

def add_to_intake(request):
    if request.method == 'POST':
        form = IntakeForm(request.POST)
        if form.is_valid():
            intake = form.save(commit=False)
            intake.user = request.user
            intake.save()
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = IntakeForm()
    return render(request, 'add_to_intake.html', {'form': form})

def success(request):
    return render(request, 'success.html')