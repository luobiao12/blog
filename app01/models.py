from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True, verbose_name='手机号')
    image = models.FileField(upload_to='images/', default='/images/default.png', verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    blog = models.OneToOneField(to='Blog', to_field='nid', verbose_name='关联Blog信息',null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='个人博客标题')
    site = models.CharField(max_length=64, verbose_name='个人博客后缀')
    theme = models.CharField(max_length=64, verbose_name='博客主题')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客信息表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='文章标题')
    desc = models.CharField(max_length=500, verbose_name='文章描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(to='UserInfo', to_field='nid', verbose_name='作者')

    comment_count=models.IntegerField(default=0,verbose_name='评论数')
    up_count=models.IntegerField(default=0,verbose_name='点赞数')
    down_count=models.IntegerField(default=0,verbose_name='踩灭数')

    category = models.ForeignKey(to='ArticleCategory', to_field='nid', null=True, verbose_name='文章所属分类')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to='Article', to_field='nid')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "文章详情表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    """
    w文章与标签多对多的详情
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    def __str__(self):
        v = self.article.title + "--" + self.tag.title
        return v

    class Meta:
        verbose_name = "文章与标签多对多表"
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = [
            ('article', 'tag'),
        ]


class ArticleCategory(models.Model):
    """
    文章分类表信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='分类标题')
    blog = models.ForeignKey(to='Blog', to_field='nid', verbose_name='所属博客')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章分类表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    文章标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='文章标签名')
    blog = models.ForeignKey(to='Blog', to_field='nid', verbose_name='关联博客')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', verbose_name='评论者', to_field='nid')
    article = models.ForeignKey(to='Article', verbose_name='评论文章', to_field='nid')
    content = models.CharField(max_length=1000, verbose_name='评论内容')
    content_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent_comment = models.ForeignKey(to='self', null=True,verbose_name='父级评论ID', to_field='nid')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论表'
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Like(models.Model):
    """
    文章点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', verbose_name='点赞用户', to_field='nid')
    like_article = models.ForeignKey(to='Article', verbose_name='点赞文章', to_field='nid')
    type = models.BooleanField(default=True, verbose_name='点赞类型')

    def __str__(self):
        return '点赞表'

    class Meta:
        verbose_name = '点赞表'
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = [('like_article','user', ),]
