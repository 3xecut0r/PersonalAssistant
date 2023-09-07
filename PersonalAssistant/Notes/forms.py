from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    ModelMultipleChoiceField,
    Form,
)

from django.contrib.auth.models import User
from Notes.models import (
    Tag,
    Note,
)

# from Users.models import User


class TagForm(ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class NoteForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=Tag.objects.none(), required=False)

    class Meta:
        model = Note
        fields = ["title", "content", "tags"]

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.user = User.objects.get(id=1)  # Временное жесткое присвоение пользователя
        # self.fields["tags"].queryset = Tag.objects.filter(user=self.user)
        self.user = user
        self.fields["tags"].queryset = Tag.objects.filter(user=self.user)

    def save(self, commit=True):
        note = super().save(commit=False)
        note.user = self.user
        if commit:
            note.save()
            self.save_m2m()
        return note


class NoteSearchForm(Form):
    search = CharField(required=False)
    include_tags = CharField(required=False)
    exclude_tags = CharField(required=False)
