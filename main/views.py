from django.shortcuts import render

from main.models import Photo, Resume


def make_rows(input_list, columns):
    new_list = list()
    while len(input_list) > columns:
        new_list.append(input_list[:columns])
        input_list = input_list[columns:]
    if input_list:
        new_list.append(input_list)
    return new_list


def resume(request):
    resume = Resume.objects.get(title='Junior Python Developer')
    candidate = resume.person
    hard_skills = [skill.title for skill in resume.hard_skills.all()]
    context = {
        'candidate': {
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'patronymic': candidate.patronymic,
            'desired_position': resume.desired_position,
            'phonenumber': candidate.phonenumber,
            'email': candidate.email,
            'github': candidate.github,
            'photo': Photo.objects.filter(person=candidate).first().image.url
        },
        'hard_skills': make_rows(hard_skills, 3)
    }
    return render(request, 'resume.html', context=context)