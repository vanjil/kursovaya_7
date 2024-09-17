from django.core.paginator import Paginator
from django.shortcuts import render
from models import Habit

def habit_list(request):
    habit_list = Habit.objects.all()
    paginator = Paginator(habit_list, 5)  # 5 привычек на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'habit_list.html', {'page_obj': page_obj})

