from django import forms

class YouTubeDownloadForm(forms.Form):
    url = forms.URLField(
        label="YouTube URL",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'Enter YouTube URL...'
        })
    )
    format = forms.ChoiceField(
        choices=[
            # ('mp4', 'MP4'), 
            ('mp3', 'MP3')],
        label="Format",
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )