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

    # Checking if the user is following the pathway, used for FollowPathway feature functionality
    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False

    # Handling form submission
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
            # Fetching tasks for authenticated users
            to_study_tasks = StudyTask.objects.filter(user=request.user, is_completed=False, pathway=pathway)
            completed_tasks = StudyTask.objects.filter(user=request.user, is_completed=True, pathway=pathway, is_visible=True)
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


def single_task_view(request, pathway_id, task_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    task = get_object_or_404(StudyTask, id=task_id, user=request.user, pathway=pathway)

    # Checking if the task has been added to revisions, if added, retrieve revision details
    is_added_to_revision = Revision.objects.filter(study_task=task).exists()

    revision_status = None
    completed_revisions = ["None"]
    revision_date_added = None
    task_retention_rate = 0

    # Checking if the user is following the pathway, used for FollowPathway feature functionality
    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False

    # Fetching revision details if the task is added to revisions
    if is_added_to_revision:
        revisions_for_task = Revision.objects.filter(study_task=task)
        first_revision_entry = revisions_for_task.first()
        revision_date_added = first_revision_entry.created_date
        task_retention_rate = first_revision_entry.retention_rate
        revision_status = first_revision_entry.overall_status
        
        # Determine which revisions are completed
        for revision in revisions_for_task:
            if revision.first_revision_status == Revision.COMPLETED:
                completed_revisions.append("FIRST")
                completed_revisions.remove("None")
            if revision.second_revision_status == Revision.COMPLETED:
                completed_revisions.append("SECOND")
            if revision.third_revision_status == Revision.COMPLETED:
                completed_revisions.append("THIRD")
            if revision.fourth_revision_status == Revision.COMPLETED:
                completed_revisions.append("FOURTH")

    count_of_revisions = 0

    # Calculating the count of completed revisions
    if "None" in completed_revisions:
        count_of_revisions = 0
    else:
        count_of_revisions = len(completed_revisions)
        

    context = {
        'task': task,
        'pathway': pathway,
        'is_added_to_revision':is_added_to_revision,
        'revision_status': revision_status,
        'completed_revisions': completed_revisions,
        'revision_date_added': revision_date_added,
        'count_of_revisions': count_of_revisions,
        'task_retention_rate': task_retention_rate,
        'is_user_following': is_user_following,
    }

    return render(request, 'pathways/single_task_template.html', context)


def delete_task_view(request, pathway_id, task_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    task = get_object_or_404(StudyTask, id=task_id, user=request.user, pathway=pathway)
    task.delete()
    return redirect('planning', pathway_id=pathway_id)
    

def complete_task_view(request, pathway_id, task_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    task = get_object_or_404(StudyTask, id=task_id, user=request.user, pathway=pathway)
    task.is_completed = True
    task.save()
    return redirect('planning', pathway_id=pathway.id)

def clear_completed_tasks(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    completed_tasks = StudyTask.objects.filter(pathway=pathway, user=request.user, is_completed=True)
    completed_tasks.update(is_visible=False)
    return redirect('planning', pathway_id=pathway.id)


def revision_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    error_message = None
    user_revisions = []
    completed_revisions = []

    # Checking if the user is following the pathway, used for FollowPathway feature functionality
    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False  

    # Fetching revisions for authenticated users
    if request.user.is_authenticated:
        if not (FollowedPathway.objects.filter(user=request.user, pathway=pathway).exists() or pathway.user == request.user):
            error_message = "You need to follow this pathway to plan or revise."
        else:
            user_revisions = Revision.objects.filter(study_task__user=request.user, study_task__pathway=pathway_id, overall_status=Revision.PENDING).order_by('due_date')
            completed_revisions = Revision.objects.filter(study_task__user=request.user, study_task__pathway=pathway_id, overall_status=Revision.COMPLETED).order_by('due_date')
    else:
        user_revisions = []
        completed_revisions = []

    return render(request, 'pathways/revision_template.html', 
                  {'revisions': user_revisions, 
                   'completed_revisions': completed_revisions, 
                   'pathway':pathway, 'error_message': error_message, 
                   'is_user_following': is_user_following,})

def mark_revision_completed(request, revision_id):
    revision = get_object_or_404(Revision, id=revision_id)

    # Define mappings for revision types, statuses, and next due dates

    REVISION_TYPE_MAP = {
        Revision.FIRST: Revision.SECOND,
        Revision.SECOND: Revision.THIRD,
        Revision.THIRD: Revision.FOURTH,
        Revision.FOURTH: "completed"
    }

    REVISION_STATUS_MAP = {
        Revision.FIRST: "first_revision_status",
        Revision.SECOND: "second_revision_status",
        Revision.THIRD: "third_revision_status",
        Revision.FOURTH: "fourth_revision_status",
    }

    next_due_dates = {
        Revision.FIRST:  timedelta(days=1),
        Revision.SECOND: timedelta(days=6),
        Revision.THIRD:  timedelta(days=9),
        Revision.FOURTH: timedelta(days=14),
    }

    # For marking the current revision as completed before moving onto the next
    setattr(revision, REVISION_STATUS_MAP[revision.revision_type], Revision.COMPLETED)
    revision.save()

    # Determine the next revision type and update accordingly
    next_revision_type = REVISION_TYPE_MAP[revision.revision_type]

    if next_revision_type == "completed":
        revision.overall_status = Revision.COMPLETED
        revision.save()
    elif next_revision_type:
        revision.revision_type = next_revision_type
        revision.due_date += next_due_dates.get(next_revision_type, timedelta(days=0))
        revision.save()
    else:
        revision.status = Revision.COMPLETED
        revision.save()  

    return redirect('revision', pathway_id=revision.pathway.id)


