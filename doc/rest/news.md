###新闻接口文档

###新闻获取接口
| http method | url                     | 说明
| GET         | /api/news/[id] | 获取新闻

返回格式说明:
```
{
    "code": 0    # int, 以后会定义返回码,0表示成功
    "message":   # str,  返回说明
    "data" : {
        "id": ""    # str
        "title": ""    # str
        "url":    # str
        "brief": ""    # str
        "content": ""    # str
        "source":""    # str
        "time":    # int, timestamp
    }
}
```

###新闻列表获取接口
| http method | url                             | 说明
| GET         | /api/news/                      | 获取新闻列表,默认10条
| GET         | /api/news?&offset=0&limit=10    | 获取新闻列表,查询参数

返回格式说明:
```
{
    "code": 0    # int, 以后会定义返回码,0表示成功
    "message":   # str,  返回说明
    "data" :     # dict list, limit决定长度
        [
            {
                "id": ""    # str
                "title": ""    # str
                "url":    # str
                "brief": ""    # str
                "content": ""    # str
                "source":""    # str
                "time":    # int, timestamp
            },
            {
                "id": ""    # str
                "title": ""    # str
                "url":    # str
                "brief": ""    # str
                "content": ""    # str
                "source":""    # str
                "time":    # int, timestamp
            },
        ]
}
```
