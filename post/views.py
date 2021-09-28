# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
#渲染主页面
from post.models import Post
from django.core.paginator import Paginator
import math


def queryAll(request,num=1):
    num = int(num)

    #获取所有帖子信息
    postList = Post.objects.all().order_by('-created')

    #创建分页器对象
    pageObj = Paginator(postList,1)

    #获取当前页的数据
    perPageList = pageObj.page(num)


    #生成页码数列表
    # 每页开始页码
    begin = (num - int(math.ceil(10.0 / 2)))
    if begin < 1:
        begin = 1

    # 每页结束页码
    end = begin + 9
    if end > pageObj.num_pages:
        end = pageObj.num_pages

    if end <= 10:
        begin = 1
    else:
        begin = end - 9

    pageList = range(begin, end + 1)


    return render(request,'index.html',{'postList':perPageList,'pageList':pageList,'currentNum':num})

#阅读全文功能
def detail(request,postid):
    postid = int(postid)

    #根据postid查询帖子的详情信息
    post = Post.objects.get(id=postid)
    print post.video

    return render(request,'detail.html',{'post':post})

#根据类别id查询所有帖子
def queryPostByCid(request,cid):

    postList = Post.objects.filter(category_id=cid)
    # Post.objects.filter(category__id=cid)

    return render(request,'article.html',{'postList':postList})

#根据发帖时间查询所有帖子
def queryPostByCreated(request,year,month):

    postList = Post.objects.filter(created__year=year,created__month=month)
    return render(request,'article.html',{'postList':postList})


#缓冲方式放视频
import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.shortcuts import render


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    path = request.GET.get('path')
    if path:
        #path = 'media/videos/' + str(request.GET.get('path'))
        print path
        size = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 10
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp
    else:
        return render(request,'v_index.html')


def video(request):
    path = request.GET.get('path')
    if path:
        return render(request, 'video.html',{'key':'media/videos/' + str(request.GET.get('path'))})
    else:
        return render(request, 'v_index.html')



