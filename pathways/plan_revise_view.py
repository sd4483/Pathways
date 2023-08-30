from django.shortcuts import render, redirect, get_object_or_404
from .models import StudyTask, Pathway, Revision
from .forms import StudyTaskForm

def planning_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)

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

    to_study_tasks = StudyTask.objects.filter(user=request.user, is_completed=False, pathway=pathway)
    completed_tasks = StudyTask.objects.filter(user=request.user, is_completed=True, pathway=pathway)

    return render(request, 'pathways/planning_template.html', {
        'form': form,
        'to_study_tasks': to_study_tasks,
        'completed_tasks': completed_tasks,
        'pathway':pathway
    })


def complete_task_view(request, pathway_id, task_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    task = get_object_or_404(StudyTask, id=task_id, user=request.user, pathway=pathway)
    task.is_completed = True
    task.save()
    return redirect('planning', pathway_id=pathway.id)


def revision_view(request, pathway_id):
    user_revisions = Revision.objects.filter(study_task__user=request.user, study_task__pathway=pathway_id, status=Revision.PENDING).order_by('due_date')
    return render(request, 'pathways/revision_template.html', {'revisions': user_revisions})

