from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PathwayForm, LinkResourceForm, FileResourceForm, TextResourceForm, ImageResourceForm, PathwaySettingsForm
from .models import Pathway

# Create your views here.

def view_pathway_view(request):
    if request.user.is_authenticated:
        pathways = Pathway.objects.filter(Q(visibility='public') | Q(user=request.user))
    else:
        pathways = Pathway.objects.filter(visibility='public')
    return render(request, 'pathways/view_pathway_template.html', {'pathways': pathways})

def delete_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    pathway.delete()
    return redirect('view_pathway')


def create_pathway_view(request):
    if request.method == 'POST':
        form = PathwayForm(request.POST)
        if form.is_valid():
            pathway = form.save(commit=False)  # Temporarily save form but don't commit to database yet
            pathway.user = request.user  # Attach the current user to the pathway
            pathway.save()
            return redirect('view_pathway')
    else:
        form = PathwayForm()

    return render(request, 'pathways/create_pathway_template.html', {'form': form})

def single_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    text_resource_form = TextResourceForm(prefix='text_resource')
    image_resource_form = ImageResourceForm(prefix='image_resource')
    link_resource_form = LinkResourceForm()
    file_resource_form = FileResourceForm()

    context = {
        'pathway': pathway,
        'text_resource_form': text_resource_form,
        'image_resource_form': image_resource_form,
        'file_resource_form' : file_resource_form,
        'link_resource_form' : link_resource_form,
    }
    return render(request, 'pathways/single_pathway_template.html', context)

def resource_archive_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    text_resource_form = TextResourceForm(prefix='text_resource')
    image_resource_form = ImageResourceForm(prefix='image_resource')
    link_resource_form = LinkResourceForm()
    file_resource_form = FileResourceForm()

    context = {
        'pathway': pathway,
        'text_resource_form': text_resource_form,
        'image_resource_form': image_resource_form,
        'file_resource_form' : file_resource_form,
        'link_resource_form' : link_resource_form,
    }
    return render(request, 'pathways/resource_archive_template.html', context)

def upvote_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    pathway.upvotes += 1
    pathway.save()
    return redirect('resource_archive', pathway_id=pathway_id)

def downvote_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    pathway.downvotes += 1
    pathway.save()
    return redirect('resource_archive', pathway_id=pathway_id)


def text_resource_view(request, pathway_id):
    print(request.POST)
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
    print(request.POST)
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
    print(request.POST)
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
    print(request.POST)
    print(request.FILES)
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

def pathway_settings_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    is_creator = (request.user == pathway.user)

    if request.method == 'POST':
        form = PathwaySettingsForm(request.POST, instance=pathway)
        if form.is_valid():
            form.save()
            return redirect('pathway_settings', pathway_id=pathway_id)
        elif form.has_changed():
            form.save()
            return redirect('pathway_settings', pathway_id=pathway_id)

    else:
        form = PathwaySettingsForm(instance=pathway)

    return render(request, 'pathways/pathway_settings_template.html', {'form': form, 'pathway': pathway, 'is_creator': is_creator})