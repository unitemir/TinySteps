from django.forms.models import model_to_dict
from django.template.loader import select_template
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from tutors.models import Teachers, Goals, Monday


class MainView(View):
    def get(self, request):
        teachers_list = list(Teachers.objects.values())
        context = {
            'teachers': teachers_list
        }
        return render(request, "tutors/index.html", context)


class AboutView(View):
    def get(self, request, teacher_id=1):
        teacher = Teachers.objects.get(id=teacher_id)
        goals = Goals.objects.get(id=teacher_id)
        monday = model_to_dict(Monday.objects.get(id=teacher_id))
        m_time = list()
        free_time = 6
        for key in monday:
            if monday[key] and key != 'id':
                m_time.append(free_time)
            free_time += 2

        context = {
            'teacher': teacher,
            'goals': goals,
            'monday': m_time,
        }
        return render(request, "tutors/profile.html", context)


class GoalsView(View):
    def get(self, request, teacher_goals):
        t_g = teacher_goals
        teacher_goals = {teacher_goals: True}
        goal = list(Goals.objects.filter(**teacher_goals))
        teachers_list = list()
        for teach_id in range(len(goal)):
            teachers_list.append(Teachers.objects.get(id=goal[teach_id].id))
        context = {
            'goal': t_g,
            'teachers': teachers_list,
        }
        return render(request, "tutors/goal.html", context)


class BookingView(View):
    def get(self, request, teacher_id, teacher_free_time):
        teach = Teachers.objects.get(id=teacher_id)
        context = {
            'teacher': teach,
            'free_time': teacher_free_time,
        }
        return render(request, "tutors/booking.html", context)


class BookingDoneView(View):
    def get(self, request, teacher_id, time, name, number):
        time = 'time_'+time+'_00'
        monday = model_to_dict(Monday.objects.get(id=teacher_id))
        for key in monday:
            if monday[key] == time:
                monday[key].update(time=False)
        context = {
            'time': time,
            'name': name,
            'number': number,
        }
        return render(request, "tutors/booking_done.html", context)


