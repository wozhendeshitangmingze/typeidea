import mistune
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度太短')
        content = mistune.Markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ('nickname', 'email', 'website', 'content')
        labels = {
            'nickname': '昵称',
            'email': 'E-mail',
            'website': '网站',
            'content': '内容',
        },
        widgets = {
            'nickname': forms.widgets.Input(
                attrs={'class': 'form-control', 'style': "width: 60%;"}
            ),
             'email': forms.widgets.EmailInput(
                 attrs={'class': 'form-control', 'style': "width: 60%;"}
             ),
            'website': forms.widgets.URLInput(
                attrs={'class': 'form-control', 'style': "width: 60%;"}
            ),
            'content': forms.widgets.Textarea(
                attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
            )
        }

