from django import forms
from .models import Block

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        # 'category'はビューで処理するため、fieldsから除外
        fields = ["block_type", "content", "image", "order", "id"]
        widgets = {
            'content': forms.Textarea(attrs={"rows": 4, "placeholder": "内容を入力"}),
            'order': forms.HiddenInput(),
            'block_type': forms.HiddenInput(),
        }

BlockFormSet = forms.modelformset_factory(
    Block,
    form=BlockForm,
    extra=0,
    can_delete=True,
    can_order=True,
)