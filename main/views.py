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
    soft_skills = [{skill.title: skill.description} for skill in resume.soft_skills.all()]
    highter_education = [
        {
            'title': univercity.institution,
            'specialization': univercity.specialization,
            'department': univercity.department,
            'education_period': univercity.education_period()
        }
        for univercity in candidate.higher_education.all()
    ]
    places_of_work = [
        {
            'post': place.post,
            'duration': place.get_work_duration(),
            'company': place.company,
            'responsibilities': place.responsibilities
        }
        for place in resume.places_of_work.all()
    ]
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
        'hard_skills': make_rows(hard_skills, 3),
        'soft_skills': soft_skills,
        'higher_education': highter_education,
        'places_of_work': places_of_work,
    }
    return render(request, 'resume.html', context=context)