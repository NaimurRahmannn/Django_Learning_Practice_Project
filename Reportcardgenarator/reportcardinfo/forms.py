from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to each widget and a required attribute when applicable
        for name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            classes = (existing + ' form-control').strip()
            field.widget.attrs['class'] = classes
            if field.required:
                field.widget.attrs['required'] = 'required'
