#coding=UTF-8
from  haystack import indexes
from post.models import *

#注意格式(模型类名+Index)
class PostIndex(indexes.SearchIndex,indexes.Indexable):
    #第一个字段必须叫text
    text = indexes.CharField(document=True, use_template=True)

    #给title,content设置索引
    title = indexes.NgramField(model_attr='title')
    content = indexes.NgramField(model_attr='content')

    def get_model(self):
        #根据哪个类搜索，就返回哪个类
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('-created')