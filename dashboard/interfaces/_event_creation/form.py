from __future__ import annotations

from django import forms


class EventCreateForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label="Title",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
            }
        ),
    )

    short_description = forms.CharField(
        required=False,
        label="Short description",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "A short description that describes the event",
            }
        ),
    )

    detailed_description = forms.CharField(
        required=False,
        label="Detailed description",
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": "A detailed description that describes the event. You can personalize it with Markdown!",
            }
        ),
    )

    tags = forms.CharField(
        required=False,
        label="Tags",
        help_text="Comma-separated tags, e.g. music, networking",
        widget=forms.TextInput(
            attrs={
                "placeholder": "music, networking, technology",
            }
        ),
    )

    starts_at = forms.DateTimeField(
        label="Starts at",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )

    ends_at = forms.DateTimeField(
        label="Ends at",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )

    location_address = forms.CharField(
        max_length=255,
        label="Address",
        widget=forms.TextInput(
            attrs={
                "placeholder": "123 Main Street",
            }
        ),
    )

    location_city = forms.CharField(
        max_length=255,
        label="City",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cádiz",
            }
        ),
    )

    max_participants = forms.IntegerField(
        min_value=0,
        required=False,
        initial=0,
        label="Max participants",
        help_text="If you set a 0 limit, there is no limit.",
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0 = no limit",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            current_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{current_class} form-control"
            ).strip()

    def clean_tags(self) -> list[str]:
        raw_tags = self.cleaned_data.get("tags", "")
        return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]