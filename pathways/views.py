from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Q
from .forms import PathwayForm, LinkResourceForm, FileResourceForm, TextResourceForm, ImageResourceForm, PathwaySettingsForm, PathwayCommentsForm, PathwayRepliesForm
from .models import Pathway, Comment, Reply, FollowedPathway
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

def view_pathway_view(request):
    followed_pathways = []
    private_pathways = []
    if request.user.is_authenticated:
        followed_pathway_ids = request.user.followedpathway_set.all().values_list('pathway', flat=True)
        followed_pathways = Pathway.objects.filter(id__in=followed_pathway_ids)
        private_pathways = Pathway.objects.filter(visibility='private', user=request.user)
        pathways = Pathway.objects.filter(Q(visibility='public') | Q(user=request.user))
    else:
        pathways = Pathway.objects.filter(visibility='public')
    
    return render(request, 'pathways/view_pathway_template.html', 
                  {'pathways': pathways, 
                   'followed_pathways': followed_pathways, 
                   'private_pathways' : private_pathways,})


def delete_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    pathway.delete()
    return redirect('view_pathway')


def create_pathway_view(request):
    if request.method == 'POST':
        form = PathwayForm(request.POST)
        if form.is_valid():
            pathway = form.save(commit=False) 
            pathway.user = request.user  
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
    return render(request, 'pathways/single_pathway_template.html', context)


def upvote_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    pathway.upvotes += 1
    pathway.save()
    referer_url = request.META.get('HTTP_REFERER', reverse('resource_archive', args=[pathway_id]))
    return redirect(referer_url)

def downvote_pathway_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    pathway.downvotes += 1
    pathway.save()
    referer_url = request.META.get('HTTP_REFERER', reverse('resource_archive', args=[pathway_id]))
    return redirect(referer_url)

def pathway_comments_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    
    if request.user.is_authenticated:
        is_user_following = request.user.followedpathway_set.filter(pathway=pathway).exists()
    else:
        is_user_following = False

    if request.method == "POST" and not request.user.is_authenticated:
        return HttpResponseForbidden("You need to login to comment.")
    
    if request.method == "POST" and request.user.is_authenticated:
        parent_comment_id = request.POST.get('parent_comment_id')
        parent_comment = None
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        text = request.POST.get('text')
        Comment.objects.create(
            pathway=pathway, 
            user=request.user, 
            text=text, 
            parent_comment=parent_comment
        )
        return redirect('pathway_comments', pathway_id=pathway_id)

    comments = Comment.objects.filter(pathway=pathway, parent_comment=None)
    form = PathwayCommentsForm()
    return render(request, 'pathways/pathway_comments_template.html', {
        'pathway': pathway,
        'form': form,
        'comments': comments,
        'is_user_following': is_user_following,
    })

@login_required
def pathway_reply_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    pathway = comment.pathway

    if request.method == "POST":
        parent_reply_id = request.POST.get('parent_reply_id')
        parent_reply = None
        if parent_reply_id:
            parent_reply = get_object_or_404(Reply, id=parent_reply_id)
        
        text = request.POST.get('text')
        Reply.objects.create(
            comment=comment, 
            user=request.user, 
            text=text,
            parent_reply=parent_reply
        )
        return redirect('pathway_comments', pathway_id=pathway.id)

    form = PathwayRepliesForm()
    return render(request, 'pathways/pathway_reply_template.html', {
        'comment': comment,
        'form': form,
    })


def pathway_settings_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    is_creator = (request.user == pathway.user)

    if request.method == 'POST':
        form = PathwaySettingsForm(request.POST, instance=pathway)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('pathway_settings', pathway_id=pathway_id)
        elif form.has_changed():
            form.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('pathway_settings', pathway_id=pathway_id)

    else:
        form = PathwaySettingsForm(instance=pathway)

    return render(request, 'pathways/pathway_settings_template.html', {'form': form, 'pathway': pathway, 'is_creator': is_creator,})

def follow_pathway(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    if request.user.is_authenticated:
        FollowedPathway.objects.create(user=request.user, pathway=pathway)
        return redirect('planning', pathway_id=pathway_id)
    else:
        return HttpResponseForbidden("You need to login to follow.")
    
def unfollow_pathway(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    if request.user.is_authenticated:
        followed_pathway = FollowedPathway.objects.filter(user=request.user, pathway=pathway).first()
        if followed_pathway:
            followed_pathway.delete()
            return redirect('resource_archive', pathway_id=pathway_id)
        else:
            messages.warning(request, 'You were not following this pathway.')
            return redirect('resource_archive', pathway_id=pathway_id)
    else:
        return HttpResponseForbidden("You need to login to unfollow.")

