from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import UpdateView

from django.urls import reverse_lazy, reverse

from Notes.forms import NoteForm, TagForm, NoteSearchForm
from Notes.models import Tag, Note


def main(request):
    notes = Note.objects.filter(user=request.user)
    context = {"notes": notes}
    return render(request, "Notes/index.html", context)


@method_decorator(login_required, name="dispatch")
class BaseNoteView(View):
    model = Note

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class NoteView(BaseNoteView):
    template_name = "notes/add-note.html"
    form_class = NoteForm
    search_form_class = NoteSearchForm

    def get_context(self):
        return {
            "form": self.form_class(self.request.user),
            "search_form": self.search_form_class(),
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context())

    def post(self, request, **kwargs):
        return self.handle_note_creation(request)

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
            return render(request, self.template_name, self.get_context())

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

                return render(request, self.template_name, self.get_context())

        # Redirect to the main notes page after successful note creation
        return redirect("notes:index")


class NoteSearchView(BaseNoteView):
    template_name = "notes/search-notes.html"
    search_form_class = NoteSearchForm
    notes_per_page = 10

    def get_context(self, form=None):
        return {
            "form": form if form else self.search_form_class(),
            "search_form": self.search_form_class(),
        }

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        form = self.search_form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, self.get_context())

        search_query = form.cleaned_data.get("search", "")

        include_tags = [
            tag.strip()
            for tag in form.cleaned_data.get("include_tags", "").split(",")
            if tag.strip()
        ]
        exclude_tags = [
            tag.strip()
            for tag in form.cleaned_data.get("exclude_tags", "").split(",")
            if tag.strip()
        ]

        notes = self.get_queryset().filter().order_by("-created_at")
        # print(notes.query)
        print(notes.all())

        # Если не указаны критерии поиска, вернуть последние 10 записей
        if not (search_query or include_tags or exclude_tags):
            notes = notes[:10]
        else:
            if search_query:
                notes = notes.filter(title__icontains=search_query)
            if include_tags:
                notes = notes.filter(tags__name__in=include_tags)
            if exclude_tags:
                notes = notes.exclude(tags__name__in=exclude_tags)

        paginator = Paginator(notes, self.notes_per_page)
        context = self.get_context(form=form)
        context["page_obj"] = paginator.get_page(request.GET.get("page"))

        return render(request, self.template_name, context)


class NoteUpdateView(BaseNoteView, UpdateView):
    form_class = NoteForm
    template_name = "notes/edit-note.html"

    def get_success_url(self):
        return reverse_lazy("notes:index")

    def get_form_kwargs(self):
        kwargs = super(NoteUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class NoteRemoveView(BaseNoteView):
    template_name = "notes/confirm-delete.html"

    def get(self, request, *args, **kwargs):
        # Тут мы просто отображаем страницу подтверждения
        return render(request, self.template_name)

    # def post(self, request, *args, **kwargs):
    #     # Когда пользователь подтверждает удаление
    #     note_id = kwargs.get(
    #         "pk"
    #     )  # Предположим, что идентификатор передается как часть URL
    #     note = self.get_queryset().get(pk=note_id)
    #     note.delete()

    def post(self, request, *args, **kwargs):
        # Когда пользователь подтверждает удаление
        note_id = kwargs.get(
            "pk"
        )  # Предположим, что идентификатор передается как часть URL
        try:
            note = self.get_queryset().get(pk=note_id)
            note.delete()
        except Note.DoesNotExist:
            # Можно добавить сообщение об ошибке или просто перенаправить на главную
            pass

        return HttpResponseRedirect(reverse("notes:index"))
        # return reverse("notes:index")


class TagView(BaseNoteView):
    template_name = "notes/add-tags.html"
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

        try:
            tag.save()
            return redirect(to="notes:index")
        except IntegrityError:
            form.add_error(None, "Tag with this name already exists for the user.")
            return render(request, self.template_name, {"form": form})
