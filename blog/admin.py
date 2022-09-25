from unicodedata import category
from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Article,Category,Test,Account,Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display=('position','slug','title','status')
    search_fields= ('status','slug')
    list_filter=['status']
    prepopulated_fields={'slug':('title',)}    
    ordering=['status']
    
admin.site.register(Category,CategoryAdmin)



class ArticleAdmin(admin.ModelAdmin):
    list_display=('id','slug','title','jpublished','status','category_to_str')
    search_fields= ('description','published','status')
    list_filter=['status','published']
    prepopulated_fields={'slug':('title',)}    
    ordering=['status','published']


    def category_to_str(self, obj):
        return  " ,".join([category.title for category  in obj.category.all()]) 
    category_to_str.short_description ="category"

admin.site.register(Article,ArticleAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display=('id','slug','title','status','description','published')
    search_fields= ('description','published','status')
    list_filter=['status','published']
    prepopulated_fields={'slug':('title',)}    
    ordering=['status','published']
admin.site.register(Test,TestAdmin)



class AccountAdmin(admin.ModelAdmin):
    list_display=('age','gender','address','created')
admin.site.register(Account,AccountAdmin)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','post','created','active')
    list_filter=('active','created','updated')
    list_editable=('active',)