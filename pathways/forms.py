from django import forms
from .models import Pathway, LinkResource, FileResource, TextResource, ImageResource

class PathwayForm(forms.ModelForm):
    class Meta:
        model = Pathway
        fields = ['title', 'description']

class LinkResourceForm(forms.ModelForm):
    class Meta:
        model = LinkResource
        fields = ['title', 'notes', 'url']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['notes'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['url'].widget.attrs.update({'class': 'w-full py-2 mt-1 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})


class FileResourceForm(forms.ModelForm):
    class Meta:
        model = FileResource
        fields = ['title', 'notes', 'attachment']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['notes'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['attachment'].widget.attrs.update({'class': 'w-full py-2 mt-1 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})


class ImageResourceForm(forms.ModelForm):
    class Meta:
        model = ImageResource
        fields = ['title', 'notes', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['notes'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['image'].widget.attrs.update({'class': 'w-full py-2 mt-1 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})

class TextResourceForm(forms.ModelForm):
    class Meta:
        model = TextResource
        fields = ['title', 'content']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'w-full mb-2 mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})
        self.fields['content'].widget.attrs.update({'class': 'w-full mt-1 py-2 px-3 border border-lighter-brownish focus:outline-none focus:border-card text-stone-100 block bg-transparent rounded'})