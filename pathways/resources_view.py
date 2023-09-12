from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .forms import LinkResourceForm, FileResourceForm, TextResourceForm, ImageResourceForm
from .models import Pathway, TextResource, LinkResource, ImageResource, FileResource
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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

def resource_sorted_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    text_resource_form = TextResourceForm(prefix='text_resource')
    image_resource_form = ImageResourceForm(prefix='image_resource')
    link_resource_form = LinkResourceForm()
    file_resource_form = FileResourceForm()

    text_resources = [(resource, 'text') for resource in pathway.text_resources.all()]
    image_resources = [(resource, 'image') for resource in pathway.image_resources.all()]
    file_resources = [(resource, 'file') for resource in pathway.file_resources.all()]
    link_resources = [(resource, 'link') for resource in pathway.link_resources.all()]

    resources = text_resources + image_resources + file_resources + link_resources
    
    resources_sorted = sorted(resources, key=lambda x: x[0].created_at, reverse=True)

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
        'resources_sorted': resources_sorted,
    }
    return render(request, 'pathways/resource_sorted_template.html', context)


def text_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    text_resource_form = TextResourceForm(request.POST or None, prefix='text_resource')

    if request.method == 'POST':
        if 'text_resource' in request.POST:
            if text_resource_form.is_valid():
                text_resource = text_resource_form.save(commit=False)
                text_resource.pathway = pathway
                text_resource.created_by = request.user
                text_resource.save()

                if 'add-text' in request.path:
                    return redirect('resource_archive', pathway_id=pathway_id)
                else:
                    referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
                    return redirect(referer_url)
                
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'text_resource_form':text_resource_form})


def text_resource_delete_view(request, pathway_id, resource_id):
    text_resource = get_object_or_404(TextResource, pk=resource_id)

    if request.user != text_resource.created_by:
        raise PermissionDenied

    if request.method == "POST":
        text_resource.delete()
        referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
        return redirect(referer_url)


def link_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)

    if request.method == 'POST':
        link_resource_form = LinkResourceForm(request.POST)
        if link_resource_form.is_valid():
            link_resource = link_resource_form.save(commit=False)
            link_resource.pathway = pathway
            link_resource.created_by = request.user
            
            title, image = fetch_title_and_image(link_resource.url) 
            link_resource.fetched_title = title
            link_resource.fetched_image_url = image
            domain = extract_domain(link_resource.url)
            link_resource.fetched_domain = domain
            
            link_resource.save()

            referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
            return redirect(referer_url)
    else:
        link_resource_form = LinkResourceForm()
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'link_resource_form':link_resource_form})

def link_resource_delete_view(request, pathway_id, resource_id):
    link_resource = get_object_or_404(LinkResource, pk=resource_id)

    if request.user != link_resource.created_by:
        raise PermissionDenied

    if request.method == "POST":
        link_resource.delete()
        referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
        return redirect(referer_url)

def image_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)
    image_resource_form = ImageResourceForm(request.POST or None, request.FILES or None, prefix='image_resource')

    if request.method == 'POST':
        if 'image_resource' in request.POST:
            if image_resource_form.is_valid():
                image_resource = image_resource_form.save(commit=False)
                image_resource.pathway = pathway
                image_resource.created_by = request.user
                image_resource.save()
                referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
                return redirect(referer_url)
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'image_resource_form':image_resource_form})

def image_resource_delete_view(request, pathway_id, resource_id):
    image_resource = get_object_or_404(ImageResource, pk=resource_id)

    if request.user != image_resource.created_by:
        raise PermissionDenied

    if request.method == "POST":
        image_resource.delete()
        referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
        return redirect(referer_url)

def file_resource_view(request, pathway_id):
    pathway = get_object_or_404(Pathway, pk=pathway_id)

    if request.method == 'POST':
        file_resource_form = FileResourceForm(request.POST or None, request.FILES or None)
        if file_resource_form.is_valid():
            file_resource = file_resource_form.save(commit=False)
            file_resource.name = file_resource.attachment.name
            file_resource.pathway = pathway
            file_resource.created_by = request.user
            file_resource.save()
            referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
            return redirect(referer_url)
    else:
        file_resource_form = FileResourceForm()
    
    return render(request, 'pathways/resource_archive_template.html', {'pathway':pathway, 'file_resource_form':file_resource_form})

def file_resource_delete_view(request, pathway_id, resource_id):
    file_resource = get_object_or_404(FileResource, pk=resource_id)

    if request.user != file_resource.created_by:
        raise PermissionDenied

    if request.method == "POST":
        file_resource.delete()
        referer_url = request.META.get('HTTP_REFERER', reverse('resource_sorted', args=[pathway_id]))
        return redirect(referer_url)
    

def fetch_title_and_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string if soup.title else None

        og_title = soup.find('meta', attrs={"property": "og:title"})
        if og_title and og_title.attrs.get("content"):
            title = og_title.attrs["content"]

        image = None
        og_image = soup.find('meta', attrs={"property": "og:image"})
        if og_image and og_image.attrs.get("content"):
            image = og_image.attrs["content"]

        return title, image

    except requests.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return None, None

def extract_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri).replace("www.", "")  # remove 'www.' if it exists
    return domain