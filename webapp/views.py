import json
from django.shortcuts import render

from settings import CACHE_DIR, PROJECT_ROOT


def main(request):
    return render(request, 'root.html')

def progress(request):
    return render(request, 'progress.html', {'progress': json.loads((PROJECT_ROOT / request.GET['file']).text())})
