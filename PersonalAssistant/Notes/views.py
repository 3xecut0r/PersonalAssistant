from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.urls import reverse_lazy

from Notes.forms import NoteForm, TagForm, NoteSearchForm
from Notes.models import Tag, Note


def main(request):
    ...


@method_decorator(login_required, name="dispatch")
class BaseNoteView(View):
    model = Note

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class NoteView(BaseNoteView):
    notes_per_page = 10
    template_name = "notes/notes.html"
    template_add = "notes/add_note.html"
    form_class = NoteForm
    search_form_class = NoteSearchForm

    def get(self, request, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class(request.user),
                "search_form": self.search_form_class(),
            },
        )

    def post(self, request, **kwargs):
        if "search_submit" in request.POST:
            return self.handle_search(request)
        else:
            return self.handle_note_creation(request)

    def _search_notes(self, request, form):
        search_query = form.cleaned_data["search"]
        include_tags = form.cleaned_data["include_tags"]
        exclude_tags = form.cleaned_data["exclude_tags"]

        include_tags_list = include_tags.split(",") if include_tags else []
        exclude_tags_list = exclude_tags.split(",") if exclude_tags else []

        notes = self.model.objects.filter(user=request.user)

        if search_query:
            notes = notes.filter(title__icontains=search_query)

        if include_tags_list:
            notes = notes.filter(tags__name__in=include_tags_list)

        if exclude_tags_list:
            notes = notes.exclude(tags__name__in=exclude_tags_list)

        return notes

    def handle_search(self, request):
        form = self.search_form_class(request.POST)
        notes = (
            self._search_notes(request, form)
            if form.is_valid()
            else self.model.objects.none()
        )

        paginator = Paginator(notes, self.notes_per_page)

        context = {
            "page_obj": paginator.get_page(request.GET.get("page")),
            "form": self.form_class(request.user),
            "search_form": form,
        }

        return render(request, self.template_name, context)

    def handle_note_creation(self, request):
        """
        Handles the creation of a new note based on the POST request.

        Parameters:
        - request (HttpRequest): The request object containing form data.

        Returns:
        - HttpResponse: Rendered template response.
        """

        # Instantiate the form with posted data
        form = self.form_class(request.user, request.POST)

        # Check if the form is valid
        if not form.is_valid():
            # If not valid, re-render the template with form errors
            context = {"form": form, "search_form": self.search_form_class()}
            return render(request, self.template_name, context)

        try:
            # Create a new note but don't save to DB yet (commit=False)
            new_note = form.save(commit=False)
            # Assign the current user to the note's user field
            new_note.user = request.user
            # Save the note to the DB
            new_note.save()
            # Save many-to-many data (if any)
            form.save_m2m()

        except IntegrityError as e:
            if 'unique constraint "note of username"' in str(e):
                form.add_error(
                    "note", "This note already exists. Please add a new note."
                )
                context = {"form": form, "search_form": self.search_form_class()}
                return render(request, self.template_name, context)

        # Redirect to the main notes page after successful note creation
        return redirect("note:index")


class NoteSearchView(BaseNoteView):
    template_name = "notes/search_notes.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.search_form_class()})

    def post(self, request):
        form = self.search_form_class(request.POST)
        notes = (
            self._search_notes(request, form)
            if form.is_valid()
            else self.model.objects.none()
        )

        context = {"notes": notes, "form": form}
        return render(request, self.template_name, context)


class NoteUpdateView(BaseNoteView):
    form_class = NoteForm
    template_name = "notes/edit_note.html"
    context_object_name = "note"

    def get_queryset(self):
        # Make sure the user can only edit their own notes
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("note:index")


class NoteRemoveView(BaseNoteView):
    model = Note
    template_name = "notes/confirm_delete.html"
    context_object_name = "note"
    success_url = reverse_lazy("note:index")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TagView(BaseNoteView):
    template_name = "note/add_tags.html"
    form_class = TagForm
    model = Tag

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        tag = form.save(commit=False)
        tag.user = request.user
        tag.save()

        return redirect(to="note:index")
