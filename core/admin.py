from django.contrib import admin
from core.models import Question , Tag , Company , Post , Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Company)