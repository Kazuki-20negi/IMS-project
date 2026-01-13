from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Audiogram
from .forms import AudiogramForm
import os

@csrf_exempt  # CSRFチェックを免除する
def upload_audiogram(request):
    if request.method == 'POST':
        server_key=os.environ.get("AUDIOGRAM_API_KEY")
        client_key=request.headers.get("X-Api-Key")
        if not server_key or server_key != client_key:
            return JsonResponse({'error': '認証エラー: APIキーが違います'}, status=403)

        # 画像ファイルの取得
        original_file = request.FILES.get('original_file')
        if not original_file:
            return JsonResponse({'error': '画像ファイルがありません'}, status=400)

        # テキストデータの取得
        # main.py の payload に入っているデータを受け取る
        filename = request.POST.get('filename')
        exam_date = request.POST.get('exam_date')
        
        # 'True' という文字列が来る可能性があるので、Pythonの真偽値に変換
        need_review_str = request.POST.get('need_review', 'False')
        need_review = need_review_str == 'True'

        # 日付が 'None' という文字列で来ることがあるので対策
        if exam_date == 'None' or exam_date == '':
            exam_date = None

        # データベースへ保存
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

def audiogram_list(request):
    audiograms=Audiogram.objects.all().order_by("-created_at")
    return render(request, "audiograms/list.html", {"audiograms": audiograms})

def audiogram_edit(request, audiogram_id):
    # URLで指定されたIDのデータを取得（なければ404エラー）
    audiogram = get_object_or_404(Audiogram, pk=audiogram_id)

    if request.method == "POST":
        # 送信されたデータでフォームを更新
        # instance=audiogram を渡すことで「新規作成」ではなく「上書き」になる
        form = AudiogramForm(request.POST, instance=audiogram)
        
        if form.is_valid():
            form.save()
            return redirect('audiograms') # 一覧画面に戻る（name="audiograms"）
    else:
        # 初回表示時（GET）は、既存データをフォームに入れた状態で表示
        form = AudiogramForm(instance=audiogram)

    return render(request, 'audiograms/edit.html', {
        'form': form,
        'audiogram': audiogram
    })