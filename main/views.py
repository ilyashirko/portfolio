from django.shortcuts import render

from main.models import Person, Photo, Resume


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
            'responsibilities': place.responsibilities.split('\n')
        }
        for place in resume.places_of_work.all()
    ]
    recommendations = [
        {
            'recommender': recommendation.recommender,
            'company': recommendation.company,
            'post': recommendation.post
        }
        for recommendation in resume.recommendations.all()
    ]
    achievements = [
        {
            'title': achievement.title,
            'reached_at': achievement.reached_at,
            'company': achievement.company
        }
        for achievement in candidate.achievements.all()
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
        'about_candidate': resume.about_candidate.split('\n'),
        'recommendations': recommendations,
        'expectations': resume.expectations.split('\n'),
        'advantages': resume.advantages.split('\n'),
        'achievements': achievements,
    }
    return render(request, 'resume.html', context=context)


def biography(request):
    person = Person.objects.get(last_name='Ширко')
    biography_chapters = [
        {
            'title': chapter.title,
            'paragraphs': chapter.text.split('\n'),
            'image': chapter.photo.image.url if chapter.photo else None
        }
        for chapter in person.biography_chapters.all().order_by('index')
    ]
    context = {
        'biography': biography_chapters
    }
    return render(request, 'biography.html', context=context)


def contacts(request):
    person = Person.objects.get(last_name='Ширко')
    photo = person.photos.get(id=2)
    context = {
        'image': photo.image.url,
        'email': 'ilyashirko@gmail.com',
        'phonenumber': person.phonenumber,
        'telegram': 'https://t.me/IlyaShirko'
    }
    return render(request, 'contacts.html', context=context)


def portfolio(request):
    person = Person.objects.get(last_name='Ширко')
    projects = [
        {
            'title': project.title,
            'url': project.url,
            'description': project.short_description.split('\n'),
            'stack': [skill.title for skill in project.develop_stack.all()],
            'finished': project.finished,
            'first_image': [image.image.url for image in project.images.all()][0],
            'images': [image.image.url for image in project.images.all()][1:]
        }
        for project in person.projects.filter(will_show=True)
    ]
    context = {
        'projects': projects
    }
    return render(request, 'portfolio.html', context=context)