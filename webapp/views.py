import os
import json
import subprocess

import signal
from django.shortcuts import render, redirect

from settings import CACHE_DIR, PROJECT_ROOT

tasks = ['crawler', 'indexer']


def main(request):
    q = request.GET.get('q', '')
    return render(request, 'root.html', {'q': q}, )


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(int(pid), 0)
    except OSError:
        return False
    else:
        return True


def get_statuses():
    statuses = []
    for task in tasks:
        progress_path = CACHE_DIR / (task + '.progress')
        if progress_path.exists():
            progress = progress_path.text()
        else:
            progress = ''

        pid_path = CACHE_DIR / (task + '.pid')
        if pid_path.exists():
            pid = int(pid_path.text())
            if not check_pid(pid):
                pid = None
        else:
            pid = None

        statuses.append({'name': task, 'progress': progress, 'pid': pid})
    return statuses


def progress(request):
    statuses = get_statuses()
    return render(request, 'progress.html', {'tasks': statuses})


def start(request):
    statuses = get_statuses()
    task = request.GET['task']
    pid = [t['pid'] for t in statuses if t['name'] == task][0]
    if pid:
        return redirect('/progress')
    if task == 'crawler':
        pid = subprocess.Popen(['python', PROJECT_ROOT / 'crawler' / 'scheduler.py'], shell=True).pid
    else:
        return redirect('/progress')
    (CACHE_DIR / (task + '.pid')).write_text(str(pid))
    return redirect('/progress')

def kill(request):
    statuses = get_statuses()
    task = request.GET['task']
    pid = [t['pid'] for t in statuses if t['name'] == task][0]
    if pid:
        os.kill(int(pid), signal.SIGKILL)

    return redirect('/progress')
