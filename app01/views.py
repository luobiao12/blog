from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from django.contrib import auth
from django.http import JsonResponse


###########################################################
# 登陆部分开始-------------------------------------------------------
def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")  # 获取输入的字符串
        res = {"state": False, "msg": None}  # 自定义两个状态，方便返回，以及使用
        valid_str = request.session.get("valid_str")  # 从session里面获取随机生成的字符串
        if valid_code.upper() == valid_str.upper():
            user = auth.authenticate(username=user, password=pwd)  # 验证用户名密码是否正确
            if user:
                res["state"] = True
                auth.login(request, user)
            else:
                res["msg"] = "用户名或密码错误"
        else:
            res["msg"] = "验证码错误"
        return JsonResponse(res)
    return render(request, "login.html")


    # 生成图片部分开始------------------------------------------


def get_valid_img(request):
    import PIL #PIL就是pillow做一些图片
    from PIL import Image, ImageDraw, ImageFont
    import random
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    image = Image.new("RGB", (250, 40), get_random_color())
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/font/kumo.ttf", size=32)
    temp = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((24 + i * 36, 0), random_char, get_random_color(), font=font)
        # draw.text((24 + i * 36, 0), random_char, get_random_color())

        # 保存随机字符
        temp.append(random_char)

    # 噪点噪线
    width = 250
    height = 40
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(5):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 在内存中临时生成图片
    from io import BytesIO
    f = BytesIO()
    image.save(f, "png")
    date = f.getvalue()
    f.close()

    valid_str = "".join(temp)
    request.session["valid_str"] = valid_str
    return HttpResponse(date)


    # 生成图片部分结束------------------------------------------


# 登陆部分结束-------------------------------------------------------

###########################################################

# 注册部分开始-------------------------------------------------------
from django import forms
from django.forms import widgets
from .models import UserInfo
from django.http import JsonResponse
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# forms表单定义的类
class RegForm(forms.Form):
    user = forms.CharField(max_length=8, label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}),
                           error_messages={
                               "required": "用户名不能为空",
                               "max_length": "用户名最多8位"

                           }
                           )
    pwd = forms.CharField(min_length=4, label="密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages={
                              "required": "密码不能为空",
                              "min_length": "密码最短4位"
                          }
                          )
    repeat_pwd = forms.CharField(min_length=4, label="确认密码",
                                 widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                                 error_messages={
                                     "required": "请确认密码",
                                     "min_length": "密码最短4位"
                                 }
                                 )
    email = forms.EmailField(label="邮箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control  "}),
                             error_messages={
                                 "required": "邮箱不能为空"
                             }
                             )

    def clean_user(self):
        val = self.cleaned_data.get("user")  # 获取输入的用户名
        ret = UserInfo.objects.filter(username=val)  # 验证用户名是否存在
        if not ret:
            return val
        else:
            raise ValidationError("该用户已存在")

    def clean(self):
        if self.cleaned_data.get("pwd") == self.cleaned_data.get("repeat_pwd"):  # 判断两次密码是否相同
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致！")


def reg(request):
    if request.method == "POST":
        # if  request.is_ajax():
        res = {"user": None, "error_dict": None}  # 定义两个对象
        form = RegForm(request.POST)  # 获取POST传过来的值
        if form.is_valid():  # 判断传过来的值是否合格
            print(form.cleaned_data)  # 传过来的所有干净的值
            print(request.FILES)
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            image = request.FILES.get("image")
            print("user", user)
            print("avatar", image)
            if image:  # 如果用户上传了头像，则创建
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email, image=image)
            else:  # 如果用户没有上传头像，默认使用原始头像
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            res["user"] = user.username
        else:
            # print(form.errors)
            print(form.cleaned_data)
            res["error_dict"] = form.errors  # 所有的错误信息都放在errors里面
        return JsonResponse(res)  # 返回的是一个字典
    form = RegForm()  # 调用forms定义的类
    return render(request, "reg.html", locals())


# 注册部分结束---------------------------------------------------------

###########################################################

# 博客主页部分开始----------------------------------------------------------

from .models import *


def index(request):
    article_list = Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


# 博客主页部分结束----------------------------------------------------------

###########################################################


# 个人站点开始--------------------------------------------------------

###########################################################
from django.db.models.functions import ExtractMonth, TruncMonth, TruncYear  # 导入查询年月的模块


def homesite(request, username, **kwargs):
    print(username)
    print(kwargs)
    # 当前站点用户对象
    user = UserInfo.objects.filter(username=username).first()
    print(user)
    if not user:
        return HttpResponse("4404")
    # 当前站点对象
    blog = user.blog
    print(blog)
    if not kwargs:
        # 查询当前站点的所有文章
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get("condition")
        print(condition)
        params = kwargs.get("params")
        month = kwargs.get("month")
        if condition == "cate":
            article_list = Article.objects.filter(user=user).filter(category__title=params)
        elif condition == "tag":
            article_list = Article.objects.filter(user=user).filter(tags__title=params)
        else:
            article_list = Article.objects.filter(user=user).filter(create_time__year=params, create_time__month=month)

    return render(request, "homesite.html", locals())


# 个人站点结束--------------------------------------------------------

###########################################################

# 文章详情开始--------------------------------------------------------
def article_detail(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()  # 获取的是当前登陆的用户名
    print(user)
    blog = user.blog  # 拿到的是某个人的个人博客
    print(blog)
    article = Article.objects.filter(pk=article_id).first()  # 拿到的是博客的标题
    print(article)
    comment_list = Comment.objects.filter(article_id=article_id)
    return render(request, "article_detail.html", locals())


# 文章详情结束--------------------------------------------------------


###########################################################

# 点赞开始--------------------------------------------------------

import json
from django.http import JsonResponse
from django.db.models import F
from django.db import transaction


def poll(request):
    is_up = json.loads(request.POST.get("is_up"))
    article_id = request.POST.get("article_id")
    print(article_id)
    user_id = request.user.pk
    res = {"state": True}
    try:
        with transaction.atomic():
            Like.objects.create(type=is_up, like_article_id=article_id, user_id=user_id)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:
        res["state"] = False
        res["first_operate"] = Like.objects.filter(like_article_id=article_id, user_id=user_id).first().type
    return JsonResponse(res)


    # 点赞结束--------------------------------------------------------


    ###########################################################


    # 评论开始--------------------------------------------------------


def comment(request):
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    user_id = request.user.pk
    res = {"state": True}
    with transaction.atomic():
        if not pid:  # 提交根评论
            obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, )
        else:  # 提交子评论
            obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)
    res["time"] = obj.content_time.strftime("%Y-%m-%d %H:%M")
    res["content"] = obj.content
    # import json
    return JsonResponse(res)

    # 评论楼


def get_comment_tree(request, id):
    print(111111)
    ret = list(Comment.objects.filter(article_id=id).values("pk", "content", "parent_comment_id", "user__username"))
    print("*" * 120, ret)
    print(222222)
    return JsonResponse(ret, safe=False)
    # 评论结束--------------------------------------------------------


    ###########################################################

    # 后台管理开始--------------------------------------------------------


def add_article(request, username):
    if request.method == 'POST':
        article_title = request.POST.get('article_title')
        article_detail = request.POST.get("article_detail")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(article_detail, "html.parser")
        # 过滤
        for tag in soup.find_all():
            if tag.name == "script":
                tag.decompose()
        print(123)
        print(request.user)
        article_obj = Article.objects.create(title=article_title, user=request.user, desc=soup.text[0:150])
        print(1234)
        ArticleDetail.objects.create(content=soup.prettify(), article=article_obj)
        return redirect("/blog/" + username)
    else:
        return render(request, "add_article.html")


from blog import settings


def upload_img(request):
    img_obj = request.FILES.get('img')
    import os
    media_path = settings.MEDIA_ROOT
    path = os.path.join(media_path, 'article_imgs', img_obj.name)
    with open(path, 'wb') as f:
        for line in img_obj:
            f.write(line)
        f.close()
    res = {
        'url': '/media/article_imgs/' + img_obj.name,
        'error': 0
    }
    import json
    return HttpResponse(json.dumps(res))
