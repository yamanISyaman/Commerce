from django import forms

style = "width: 28vw;"


class CreateForm(forms.Form):
    title = forms.CharField(
        strip=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Title",
            "style": style
        }))
    price = forms.FloatField(
        min_value=0.5,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Price",
            "style": style
        }))
    description = forms.CharField(
        strip=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Description",
            "style": style
        }))
    image = forms.URLField(widget=forms.URLInput(
        attrs={
            "class": "form-control",
            "placeholder": "Image Url",
            "style": style
        }))
    category = forms.ChoiceField(
        choices=[
            ("None", "None"),
            ("technical", "Technical"),
            ("kitchen", "Kitchen"),
            ("animals", "Animals"),
            ("farm", "Farm")
            ],
                                 widget=forms.Select(attrs={
                                     "class": "form-control",
                                     "style": style
                                 }))


class BidForm(forms.Form):
    bid = forms.FloatField(
        min_value = 0.5,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Bid",
            "style": style
        }))


class CommentForm(forms.Form):
    comment = forms.CharField(
        strip=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Comment",
            "style": style
        }))