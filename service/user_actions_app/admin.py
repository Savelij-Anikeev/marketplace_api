from django.contrib import admin
from .models import Question, Review, Answer

admin.site.register(Review)
admin.site.register(Question)
admin.site.register(Answer)
