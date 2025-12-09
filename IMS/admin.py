from django.contrib import admin
# Categoryをインポートに追加
from .models import Page, Category, Block

admin.site.register(Page)
admin.site.register(Category) # この行を追加
admin.site.register(Block)