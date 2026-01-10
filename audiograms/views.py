from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Audiogram

@csrf_exempt  # CSRFチェックを免除する（重要）
def upload_audiogram(request):
    if request.method == 'POST':
        # 1. 画像ファイルの取得
        # main.py では files={"original_file": f} で送っているので、ここで受け取る
        original_file = request.FILES.get('original_file')

        if not original_file:
            return JsonResponse({'error': '画像ファイルがありません'}, status=400)

        # 2. テキストデータの取得
        # main.py の payload に入っているデータを受け取る
        filename = request.POST.get('filename')
        exam_date = request.POST.get('exam_date')
        
        # 'True' という文字列が来る可能性があるので、Pythonの真偽値に変換
        need_review_str = request.POST.get('need_review', 'False')
        need_review = need_review_str == 'True'

        # 日付が 'None' という文字列で来ることがあるので対策
        if exam_date == 'None' or exam_date == '':
            exam_date = None

        # 3. データベースへ保存
        try:
            new_audiogram = Audiogram.objects.create(
                original_file=original_file,
                filename=filename,
                exam_date=exam_date,
                need_review=need_review
            )
            return JsonResponse({'message': '保存成功', 'id': new_audiogram.id}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POSTメソッドのみ許可されています'}, status=405)