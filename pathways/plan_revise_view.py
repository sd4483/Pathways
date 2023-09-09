from datetime import timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import StudyTask, Pathway, Revision, FollowedPathway
from .forms import StudyTaskForm

def planning_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    error_message = None
    to_study_tasks = []
    completed_tasks = []

    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False

    if request.method == "POST":
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.pathway = pathway
            task.save()
            return redirect('planning', pathway_id=pathway_id)
    else:
        form = StudyTaskForm()

    if request.user.is_authenticated:
        if not (FollowedPathway.objects.filter(user=request.user, pathway=pathway).exists() or pathway.user == request.user):
            error_message = "You need to follow this pathway to plan or revise."
        else:
            to_study_tasks = StudyTask.objects.filter(user=request.user, is_completed=False, pathway=pathway)
            completed_tasks = StudyTask.objects.filter(user=request.user, is_completed=True, pathway=pathway)
    else:
        to_study_tasks = []
        completed_tasks = []

    return render(request, 'pathways/planning_template.html', {
        'form': form,
        'to_study_tasks': to_study_tasks,
        'completed_tasks': completed_tasks,
        'pathway':pathway,
        'error_message': error_message,
        'is_user_following': is_user_following,
    })


def complete_task_view(request, pathway_id, task_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    task = get_object_or_404(StudyTask, id=task_id, user=request.user, pathway=pathway)
    task.is_completed = True
    task.save()
    return redirect('planning', pathway_id=pathway.id)


def revision_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    error_message = None
    user_revisions = []
    completed_revisions = []

    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False  
          
    if request.user.is_authenticated:
        if not (FollowedPathway.objects.filter(user=request.user, pathway=pathway).exists() or pathway.user == request.user):
            error_message = "You need to follow this pathway to plan or revise."
        else:
            user_revisions = Revision.objects.filter(study_task__user=request.user, study_task__pathway=pathway_id, status=Revision.PENDING).order_by('due_date')
            completed_revisions = Revision.objects.filter(study_task__user=request.user, study_task__pathway=pathway_id, status=Revision.COMPLETED).order_by('due_date')
    else:
        user_revisions = []
        completed_revisions = []

    total_retention = sum(revision.retention_rate for revision in user_revisions)
    average_retention = total_retention / len(user_revisions) if user_revisions else 0

    return render(request, 'pathways/revision_template.html', 
                  {'revisions': user_revisions, 
                   'completed_revisions': completed_revisions, 
                   'pathway':pathway, 'error_message': error_message, 
                   'is_user_following': is_user_following, 
                   'average_retention': average_retention})

def mark_revision_completed(request, revision_id):
    revision = get_object_or_404(Revision, id=revision_id)
    
    REVISION_TYPE_MAP = {
        Revision.FIRST: Revision.SECOND,
        Revision.SECOND: Revision.THIRD,
        Revision.THIRD: Revision.FOURTH,
        Revision.FOURTH: "completed"
    }

    next_due_dates = {
        Revision.FIRST:  timedelta(days=1),
        Revision.SECOND: timedelta(days=6),
        Revision.THIRD:  timedelta(days=9),
        Revision.FOURTH: timedelta(days=14),
    }

    next_revision_type = REVISION_TYPE_MAP[revision.revision_type]

    if next_revision_type == "completed":
        revision.status = Revision.COMPLETED
        revision.save()
    elif next_revision_type:
        revision.revision_type = next_revision_type
        revision.due_date += next_due_dates.get(next_revision_type, timedelta(days=0))
        revision.save()
    else:
        revision.status = Revision.COMPLETED
        revision.save()  

    return redirect('revision', pathway_id=revision.pathway.id)


