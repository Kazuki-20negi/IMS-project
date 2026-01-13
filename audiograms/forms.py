from django import forms
from .models import Audiogram

class AudiogramForm(forms.ModelForm):
    class Meta:
        model = Audiogram
        # 編集させたい項目
        fields = ['filename', 'exam_date', 'need_review', 'memo']
        
        # カレンダー入力など、見た目の調整（widgets）
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}), # カレンダーが出るようになる
            'memo': forms.Textarea(attrs={'rows': 4}),
        }
        # ラベルのカスタマイズ
        labels = {
            'filename': 'ファイル名',
            'exam_date': '検査日',
            'need_review': '要確認フラグ',
            'memo': 'メモ',
        }