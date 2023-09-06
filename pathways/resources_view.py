from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import LinkResourceForm, FileResourceForm, TextResourceForm, ImageResourceForm
from .models import Pathway
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def resource_archive_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    text_resource_form = TextResourceForm(prefix='text_resource')
    image_resource_form = ImageResourceForm(prefix='image_resource')
    link_resource_form = LinkResourceForm()
    file_resource_form = FileResourceForm()

    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False

    context = {
        'pathway': pathway,
        'text_resource_form': text_resource_form,
        'image_resource_form': image_resource_form,
        'file_resource_form' : file_resource_form,
        'link_resource_form' : link_resource_form,
        'is_user_following': is_user_following,
    }
    return render(request, 'pathways/resource_archive_template.html', context)

def text_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    text_resource_form = TextResourceForm(request.POST or None, prefix='text_resource')

    if request.method == 'POST':
        if 'text_resource' in request.POST:
            if text_resource_form.is_valid():
                text_resource = text_resource_form.save(commit=False)
                text_resource.pathway = pathway
                text_resource.save()
                return redirect('resource_archive', pathway_id=pathway_id)
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'text_resource_form':text_resource_form})

def link_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)

    if request.method == 'POST':
        link_resource_form = LinkResourceForm(request.POST)
        if link_resource_form.is_valid():
            link_resource = link_resource_form.save(commit=False)
            link_resource.pathway = pathway
            link_resource.save()
            return redirect('resource_archive', pathway_id=pathway_id)
    else:
        link_resource_form = LinkResourceForm()
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'link_resource_form':link_resource_form})


def image_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    image_resource_form = ImageResourceForm(request.POST or None, request.FILES or None, prefix='image_resource')

    if request.method == 'POST':
        if 'image_resource' in request.POST:
            if image_resource_form.is_valid():
                image_resource = image_resource_form.save(commit=False)
                image_resource.pathway = pathway
                image_resource.save()
                return redirect('resource_archive', pathway_id=pathway_id)
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'image_resource_form':image_resource_form})

def file_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)

    if request.method == 'POST':
        file_resource_form = FileResourceForm(request.POST or None, request.FILES or None)
        if file_resource_form.is_valid():
            file_resource = file_resource_form.save(commit=False)
            file_resource.pathway = pathway
            file_resource.save()
            return redirect('resource_archive', pathway_id=pathway_id)
    else:
        file_resource_form = FileResourceForm()
        
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'file_resource_form':file_resource_form})