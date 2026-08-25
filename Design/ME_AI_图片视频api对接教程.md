# ME AI 图片视频api对接教程

# 一、网站信息

## 中转站地址（baseUrl）： [https://api\.meai\.cloud](https://api.meai.cloud)

加速地址\(访问慢或者频繁524报错用这个\)：https://cn\.meai\.cloud 

#### 额度购买 自动发货 10元 300刀 [ME AI 大模型api中转站的小店](https://pay.ldxp.cn/shop/YSR74HU9)

### [点击查看支持的模型和价格列表](https://api.meai.cloud/pricing)

# 二、注册登录账户

浏览器访问中转站地址 https://api\.meai\.cloud

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OWE4MWZmZjBkZDUyZWJhZmNjYjdiY2I1YTIyMDk0ODNfYjFhNDYwZWI0M2JiMDFmYWM4ZGI2ZTg0YzRjNjNlZDNfSUQ6NzY0NjI4MjE0ODI3MzcyMDUzMV8xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)

第一步：注册一个账户根据个人喜好填写，用户名,密码 （一定要记住用户名，不然找回不了）

第二步：注册完之后登陆刚刚注册好的账户

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTk1ODIxYWU0ZmU4NWNmMmI0NmUyY2IxNmQwM2ZiNWRfZTNhZjhkNzJhMTcwZDhkYzk1ZTJmYjU3MTQzMDAxZjdfSUQ6NzY0NjI4MjE0NzkwODc5OTQxOF8xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGJlN2EyYmNlNWM1MWJmZWNmZmEwZGIxNGIxMmYwYWZfZDg1Nzg4NzExZmFlYTZmYzM1OTkzZWRhODk5OTcyOGNfSUQ6NzY0NjI4MjE0Nzc5NTc1MDEwM18xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)

---

# 三、登录后领取令牌

第三步：点击钱包管理，兑换额度

兑换完之后你会看到当前额度

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NThhZDJkNmVmMDk4MGUxNjYyMTNhMzBiODY0ZDM4ZDFfNTRiMjk4NjcyY2JlMzAwOTVjNGYzNDMxNGI1NWNlMzlfSUQ6NzY0NjI4MjE0OTExNjg1NzMwOF8xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)

兑换完之后

第四步：点击令牌管理，然后点击添加令牌

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=M2I5Y2NiNzU0YTljMTk0NDc1YTI2MTAzZTQyZDdmNzBfNmVmMzY0ODUzMjUzY2Y1Y2MwZjk3NDkyZWQ1ZTIzY2VfSUQ6NzY0NjI4MjE1MDg4Njc3MTkxN18xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)

**打开添加令牌之后**

**名称：随便填**

**令牌分组：默认分组hu**

**过期时间：默认**

**新建数量：默认**

**额度设置：默认**

**无限额度：默认**

**模型限制列表：不要开启！！！**



**最后一步点击提交**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGZiYmYxZWQ2NWIyN2NiODE4NDI3OWY0ZjY3ZTAxOWZfMWQ1NTBiNjRhYWE1ZmJjNzg1NGE2OTIwZmI4OGJlNWVfSUQ6NzY0NjI4MjE0OTM0NzQ5NDg3NF8xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)



![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTdmZDg4ZmM1YjFhYWVjZDdlYjdkYWM2Y2Y5NTA3NjFfNjkzY2JjNmZjODY5ZTc3MWRhNjA4YWEwYTc2ZDRjMTRfSUQ6NzY0NjI4MjE0ODUwODc5ODE1MV8xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)



令牌内容为sk\-xxxx

# 四、开始创作

登录网站后点击“图片视频创作”，输入网站令牌，即可创作图片和视频

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTZiZDM2YmJhYjk3YWEwY2JlYWE5ZjJiZTZmYzMzMTdfZDlhYjMzMWYyMjVlODc0NzhlODMzZTZiOGM4MjQwN2JfSUQ6NzY0NjI4MjYxNDAzMDIwODIwM18xNzgxMzIxOTM0OjE3ODE0MDgzMzRfVjM)





# 五、api对接

所有请求都需要带请求头 Authorization：Bearer sk\-xxx

生图模型：seedream\-5\.0，seedream\-4\.5

视频模型：seedance\-2\.0，happyhorse\-1\.0，wan2\.7



生图

POST https://api\.meai\.cloud/v1/images/generations/async

文生图

\{

"model": "seedream\-5\.0",

"input": \{

"messages": \[

\{

"role": "user",

"content": \[

\{"text": "一只小猫"\}

\]

\}

\]

\},

"parameters": \{

"size": "2048\*2048",

"n": 1,

"watermark": false,

"thinking\_mode": false

\}

\}

图生图

\{

"model": "seedream\-5\.0",

"input": \{

"messages": \[

\{

"role": "user",

"content": \[

\{"image": "图片的http/https地址"\},

\{"text": "将图片中的人物换成白色衣服"\}

\]

\}

\]

\},

"parameters": \{

"size": "2048\*2048",

"n": 1,

"watermark": false

\}

\}



返回

\{

"id": "62c0a549\-1780\-4094\-9c97\-a09c3047b543",

"task\_id": "62c0a549\-1780\-4094\-9c97\-a09c3047b543",

"object": "",

"model": "",

"status": "PENDING",

"progress": 0,

"created\_at": 0

\}



查询异步生图情况\(每次查询间隔时间在20秒以上\)

GET https://api\.meai\.cloud/v1/images/\{task\_id\}



返回\-生成中

\{

"created\_at": 1780210388,

"id": "0df30938\-814d\-9183\-a623\-b1307d6db2f9",

"object": "",

"status": "RUNNING"

\}

返回\-生成完成

\{

"created\_at": 1780210388,

"id": "18ba2548\-d95a\-9596\-976b\-9442d65b2d83",

"object": "https://xxx",

"status": "SUCCEEDED"

\}





生视频 POST https://api\.meai\.cloud/v1/videos

文生视频

\{

"model": "seedance\-2\.0",

"input": \{

"prompt": "小猫"

\},

"parameters": \{

"resolution": "1080P",

"ratio": "16:9",

"prompt\_extend": false,

"watermark": false,

"duration": 15

\}

\}



图生视频\(首帧生视频\)

\{

"model": "seedance\-2\.0",

"input": \{

"prompt": "图片中的人物开始跳舞",

"media": \[

\{

"type": "first\_frame",

"url": "http/https地址"

\}

\]

\},

"parameters": \{

"resolution": "1080P",

"duration": 10,

"prompt\_extend": true,

"watermark": false

\}

\}



首尾帧生视频\(只有wan2\.7模型支持\)

\{

"model": "wan\-2\.7",

"input": \{

"prompt": "图片中的人物在奔跑",

"media": \[

\{

"type": "first\_frame",

"url": "图片的http/https地址"

\},

\{

"type": "last\_frame",

"url": "图片的http/https地址"

\}

\]

\},

"parameters": \{

"resolution": "1080P",

"duration": 15,

"prompt\_extend": false,

"watermark": false

\}

\}



参考生视频，支持参考首帧，尾帧，音频，视频，角色图片，九宫格图片等

\{

"model": "seedance\-2\.0",

"input": \{

"prompt": "图1中的人物穿上图2的装饰",

"media": \[

\{

"type": "reference\_image",

"url": "图片的http/https地址"

\},

\{

"type": "reference\_image",

"url": "图片的http/https地址"

\}

\]

\},

"parameters": \{

"resolution": "1080P",

"ratio": "16:9",

"duration": 10,

"prompt\_extend": false,

"watermark": false

\}

\}



返回

\{

"id": "92f875ee\-f97b\-4941\-b4ef\-dc5f7fa60022",

"task\_id": "92f875ee\-f97b\-4941\-b4ef\-dc5f7fa60022",

"object": "",

"model": "",

"status": "PENDING",

"progress": 0,

"created\_at": 0

\}



查询视频状态\(每次查询间隔时间在20秒以上\) GET https://api\.meai\.cloud/v1/videos/\{task\_id\}



返回

生成中

\{

"created\_at": 1780213835,

"id": "38a53363\-3d0f\-9475\-a971\-f7f2fdf6a8e6",

"object": "",

"seconds": 0,

"status": "RUNNING"

\}

生成完成

\{

"created\_at": 1780213835,

"id": "2810924c\-616f\-93c6\-bc35\-9f974846caf2",

"object": "https://视频地址",

"seconds": 15,

"status": "SUCCEEDED"

\}



任务失败

\{

"id": "dd75bf76\-6ec0\-97f0\-bd02\-aa55b8806edc",

"object": "",

"status": "FAILED: Green net check failed for text \(input\): Input data may contain inappropriate content\.",

"seconds": 0,

"created\_at": 1781018152

\}



# 六、说明



图片上传需要使用http/https地址以减少请求延迟，可以使用如下免费存储

[七牛云 \| 一站式中立音视频云 \+ AI](https://s.qiniu.com/JbmIVv)



图像/视频分辨率比例值：

|宽高比|4K|2K|1K|
|---|---|---|---|
|1:1|4096\*4096|2048\*2048|1280\*1280|
|16:9|4096\*2304|2688\*1536|1696\*960|
|9:16|2304\*4096|1536\*2688|960\*1696|
|4:3|4096\*3072|2368\*1728|1472\*1104|
|3:4|3072\*4096|1728\*2368|1104\*1472|

上传的图片分辨率需要在 300x300 以上



参考生视频的参数类型

参考图像通过“图1、图2”这类标识指代，参考视频通过“视频1、视频2”这类标识指代。英文提示词则写为“Image 1”、"Video 1”这类标识。

参考图像最多5张，同参考图像 \+ 参考视频 ≤ 5，参考视频加起来总时长最多5秒

指定首帧

\{

"type": "first\_frame",

"url": "图片的http/https地址"

\},



为参考图指定音频

\{

"type": "reference\_image",

"url": "图片的http/https地址",

"reference\_voice": "音频的http/https地址"

\},



参考视频\(只有wan2\.7模型支持\)

\{

"type": "reference\_video",

"url":  "视频的http/https地址"

\},



生成失败说明

网页生成的图片视频只缓存24小时，如有需要请尽快下载保存到本地

生成失败大多是触发敏感词，如果失败又扣费了，请保留任务ID提供给售后返还额度



提示词应无违法、违规、涉政、色情、暴力、分裂、低俗、恶意引导等敏感内容，不要包含特定校名、地域名称

