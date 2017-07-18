
##1. 注意
由于学校服务器不支持PUT 和DELETE操作，所以PUT 和DELETE并入POST ,请求时以
requestMethod:POST/PUT/DELETE作为区分
##2.错误信息汇总:
    status 400，已存在(比如：用户名，角色名，节点名称，新闻属性和标签唯一，重复时返回此错误)

    status 404 Not founded
    status 401 Unauthorized
##3.用户模块
GET  /api/user/users

    [{
    id:int                  
    user_name:str,
    login_time:,（上一次登陆时间）
    login_ip:str,(上一次登陆ip)
    status:bool(该用户状态True正常，false被禁),
    email:str,
    nodes:[
    {   id:int,             
        node_name:str,
        status:bool,
        level:int
    }]
    roles:[{                是roles不是role
    id:int ,                
    role_name:str,
    status:bool,
    }
    ]

    }
    ]


POST /api/user/users

    {
    user_name:str,
    password:str
    email:str
    role_name:list(str)        注意是list
    }

GET /api/user/users/id

    {
    int: int   ,               新添加的，其实也可以不要，因为与路由的id一致,格式统一一下加上吧
     user_name:str,
    login_time:,（上一次登陆时间）
    login_ip:str,(上一次登陆ip)
    status:bool(该用户状态True正常，false被禁),
    email:str,
    nodes:[
    {    id:int,                
         node_name:str,
        status:bool,
        level:int
    }]
    roles:[{                    是roles不是role
    id:int ,                    
    role_name:str,
    status:bool,
    }
    ]
    }

PUT /api/user/users/id

    {
    user_name:str,
    password:str
    email:str
    role_name:list(str)             注意是list 
    status:bool,


    } optional

DELETE /api/user/users/id

GET /api/user/current-user           

    {
        和 Get/api/user/users/id 返回的数据一样
    }

GET /api/user/nodes

    [
    {
    id: int             
    node_name:str,
    status:bool,
    level:int
    }
    ]

GET /api/user/nodes/id

    {
    id: int             
    node_name:str,
    status:bool,
    level:int
    }
PUT /api/user/nodes/id

    {
    status :bool
    } optional

GET /api/user/roles

    [{
    id:int,             
    role_name:str,
    status:bool,
    nodes:[
        {
        id:int,          
         node_name:str,
        status:bool,
        level:int
    }
    ]
    }]

POST /api/user/roles(新建一角色)

    {
    role_name:str
    node_name:list(要添加的节点名)
    }

GET /api/user/roles/id

    {
    id:int ,             
     role_name:str,
    status:bool,
    nodes:[
        {
        id: int,        
         node_name:str,
        status:bool,
        level:int
    }
    ]
    }
PUT /api/user/roles/id

    {
    role_name:list(str),             注意是list
    status:bool,
    node_name:list
    }
    optional

DELETE /api/user/roles/id


##4.搜索模块

GET /api/Search/news?category=&tags=&start=&end=&sort

    {
        和 GET/api/news/news返回的数据格式一样
    }注:tags可以多个,start-end为搜索的时间范围,为时间戳  sort=latest/oldest 反向或正向排序



##5. template

GET /api/templates/fp:path 
> ("api/templates/admin/app.html" .eg)
##6. news

GET /api/news/news/id application/json
    
    ->

    [
        {
            id: int,
            author: str,
            category: str,
            tags: [str],
            post_time: UTC timestamp seconds,
            title: str,
            outline: str,
            editable: boolean,
        }
    ]

POST /api/news/news application/json
    
    {
        category: str,
        tags: [str],
        title: str,
        detail: str,
    }

    -> 

    HTTP state code

    200 success


GET /api/news/news/id:str

    
    ->

    {
        id: int,
        category: str,
        tags: [str],
        post_time: UTC timestamp seconds,
        title: str,
        outline: str,
        editable: boolean,

        detail: str
    }

    or

    404

PUT /api/news/news/id:str
    
    {
        category: str,
        tags: [str],
        title: str,
        outline: str,
        editable: boolean,

        detail: str
    }

    # optional keys

    ->

    HTTP state code

    200 OK


DELETE /api/news/news/id:str

    ->

    200 OK
    500 Not Authorized

    # slideshow

GET /api/news/slider-show

    ->

    [
        {
            id: int,
            post_time: UTC timestamp sec,
            title: str,
            img_url: str,               
            outline: str,
            editable: bool,
            link: str,
        }
    ]

POST /api/news/slider-show

    {
        title: str,
        img_url: str,               
        outline: str,
        link: str,
    }

PUT /api/news/slider-show/id:str

    {
        title: str,
        img_url: str,                
        outline: str,
        link: str,
        #editable: bool,
    }

    #optional keys

DELETE /api/news/slider-show/id:str

    ->

    200 OK

GET /api/news/tags

    [{
        id:int,
        name:str
    }]
POST /api/news/tags

    {
        name:str
    }
GET /api/news/tags/id

     {
        id:int,
        name:str
    }
PUT /api/news/tags/id

    {
        name：str
    }
DELETE /api/news/tags/id

GET /api/news/categorys

    [{
        id:int,
        name:str
    }]
POST /api/news/categorys

    {
        name:str
    }
GET /api/news/categorys/id

     {
        id:int,
        name:str
    }
PUT /api/news/categorys/id

    {
        name
    }

DELETE /api/news/categorys/id
