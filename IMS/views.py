from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Page, Category
from .forms import BlockFormSet # 現在のforms.pyからインポート

def home(request):
    pages = Page.objects.all()
    # 【変更点①】テンプレートに全てのページ情報を渡す
    # これにより home.html でナビゲーションを動的に作成できます
    context = {
        'pages': pages,
    }
    return render(request, 'IMS/home.html', context)

# 【変更点②】関数名を health から page_detail に変更
# これで「医療管理」以外のページも扱う汎用的なビューであることが分かりやすくなります
def page_detail(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    categories = page.categories.all()
    message = ""

    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category_to_edit = get_object_or_404(Category, id=category_id)

        formset = BlockFormSet(request.POST, request.FILES, 
                               queryset=category_to_edit.blocks.all(), 
                               prefix=f'cat-{category_id}')

        if formset.is_valid():
            instances = formset.save(commit=False)
            
            for obj in formset.deleted_objects:
                obj.delete()

            for instance in instances:
                instance.category = category_to_edit
                instance.save()
            
            saved_message = f"「{category_to_edit.title}」を保存しました"
            # 【変更点③】リダイレクト先を 'page_detail' に変更
            redirect_url = reverse('page_detail', args=[page_id]) + f"?message={saved_message}"
            return redirect(redirect_url)
        else:
            for category in categories:
                if str(category.id) == category_id:
                    category.formset = formset
                else:
                    category.formset = BlockFormSet(queryset=category.blocks.all(), prefix=f'cat-{category.id}')
    else:
        for category in categories:
            category.formset = BlockFormSet(queryset=category.blocks.all(), prefix=f'cat-{category.id}')

    if 'message' in request.GET:
        message = request.GET.get('message')

    return render(request, 'IMS/health.html', {
        "page": page,
        "categories": categories,
        "message": message,
    })