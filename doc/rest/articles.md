###articles 接口文档
设计参考
[Designing a RESTful API with Python and Flask](http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
[restful api设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
[httpapi guide](https://github.com/bolasblack/http-api-guide)

###文章获取接口
| http method | url                     | 说明
| GET         | /api/post/articles/[id] | 获取文章

返回格式说明:
```
{
    "code": 0    # int, 以后会定义返回码,0表示成功
    "message":   # str,  返回说明
    "data" : {
        "id": ""    # str
        "title": ""    # str
        "brief": ""    # str
        "content": ""    # str, markdown type
        "tag_list": []    # str list
        "source_url":    # str
    }
}
```
