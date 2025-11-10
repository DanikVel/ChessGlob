from django.contrib import admin
import blog.models as models


admin.site.register(models.Article)
admin.site.register(models.TextArticleElement)
admin.site.register(models.FileArticleElement)
admin.site.register(models.Comment)
