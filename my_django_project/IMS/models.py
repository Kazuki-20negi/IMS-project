from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0) # 表示順を管理

    class Meta:
        ordering = ['order'] # order順に並ぶように設定

    def __str__(self):
        return self.title

class Block(models.Model):
    BLOCK_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
    )
    # --- 関連付け先をPageからCategoryに変更 ---
    # 変更前: page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blocks')
    # --- ここまで ---
    
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.block_type} block"