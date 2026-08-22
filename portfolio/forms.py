from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'How can I help?'}),
    )
    message = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(
            attrs={'placeholder': 'What would you like to connect about?', 'rows': 5},
        ),
    )

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if '\n' in subject or '\r' in subject:
            raise forms.ValidationError('Enter a single-line subject.')
        return subject
