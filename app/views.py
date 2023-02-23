from django.shortcuts import render
from .services.VideosManager import get_data


def home(request):
    term = ''
    filename = f'videos_{term}_data.pickle'

    return render(request, 'app/index.html', {'videos': get_data(term, filename)})


def single_video(request, video_id):
    filename = f'video_{video_id}.pickle'

    video = get_data('', filename, video_id)

    return render(request, 'app/detail.html', {'video': video['items'][0]})


def search(request):
    term = request.GET.get('q') # + " -citizen -ntv"
    filename = f"videos_{term.replace(' ', '_')}_data.pickle"

    return render(request, 'app/search.html', {'search': term, 'videos': get_data(term, filename)})

