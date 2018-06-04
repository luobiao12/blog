from django import template
register=template.Library()
from  app01.models import *
from django.db.models.functions import ExtractMonth, TruncMonth, TruncYear  # 导入查询年月的模块
@register.inclusion_tag("memu.html")

def get_memu(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    # 查询当前站点的所有分类
    cate_list = ArticleCategory.objects.filter(blog=blog)
    # 查询每一个分类以及对应的文章数
    from django.db.models import Count
    Category_list = ArticleCategory.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    # 查询每一个标签以及对应的文章数
    tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    # 查询按年月发布的文章数,TruncMonth 返回的是datetime类型，前端需要格式化
    article_date = Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")).values("month").annotate(
        c=Count("create_time"))
    return {"username":username,"cate_list":cate_list,"Category_list":Category_list,"tag_list":tag_list,"article_date":article_date}