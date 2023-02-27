from django.shortcuts import render
from .services.VideosManager import get_data
from datetime import datetime
from django.contrib import messages


def home(request):
    term = ''
    filename = f'videos_{term}_data.pickle'

    return render(request, 'app/index.html', {'videos': get_data(term, filename)})


def single_video(request, video_id):
    filename = f'video_{video_id}.pickle'
    video = get_data('', filename, video_id)

    return render(request, 'app/detail.html', {'video': video['items'][0]})


def search(request):
    term = request.GET.get('q', '').strip() # + " -citizen -ntv"
    excludes = request.GET.get('excludes')  # + " -citizen -ntv"
    start_date = request.GET.get('start_date')  # + " -citizen -ntv"
    end_date = request.GET.get('end_date')  # + " -citizen -ntv"

    if term:
        term.replace(' ', '_')

    parameters = {}

    if request.GET.get('sort'):
        parameters['sort'] = request.GET.get('sort')

    if request.GET.get('duration'):
        parameters['duration'] = request.GET.get('duration')

    try:
        if start_date:
            parameters['publishedAfter'] = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        messages.error(request, "Please select correct start date")

    try:
        if end_date:
            parameters['publishedBefore'] = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        messages.error(request, "Please select correct end date")

    parameters['q'] = term

    if excludes is not None:
        formatted_excludes = []
        for word in excludes.replace(',', ' ').split():
            formatted_excludes.append(''.join(('-', word)))

        parameters['q'] = term + ' ' + ' '.join(formatted_excludes)

    filename = f"videos_{parameters['q'].replace(' ', '_')}_data.pickle"

    context = {
        'search_query': term,
        'parameters': request.GET,
        'videos': get_data(parameters, filename)
    }

    return render(request, 'app/search.html', context)

