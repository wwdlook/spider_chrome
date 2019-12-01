# 环境
Python3.6

## 1.功能
该项目使用webdriver爬取网站信息, 并针对有验证码的网站实现了爬取流程中人工验证的子功能，从而可以在爬虫启动后人工干预需要验证码的网页，而不必事先做好全面调查且设置完成合适的cookie。


## 2.接口

### 2.1 BaseHandler

| 函数 |   说明   |
| ---- | -------- |
| set_params | 设置参数 |
| manual_verification  | 人工验证，判断是否被导入`验证页面`以及是否人工验证完毕的依据是  请求的url是否被转向。其中判断是否被导入`验证页面`的另一项依据是  url被转向后的页面中是否含有`keyword`(可以自行设置，默认为'验证码') |
| get  | 使用ChromeDriver进行GET方法请求，`callback=`字段用于调用处理  请求完页面的自定义函数。当url为空('')时，仅保留当前页面并用于调  用下一步的自动以函数 |
| save_result  | 保存`self.result`中的结果，路径为该项目下的`data`文件夹|

### 2.2 Processor
| 函数 |   说明   |
| ---- | -------- |
| set_params | 设置参数 |
| process | 处理函数，具体功能可自行定义 |

###2.2.1 Processor_get_doc
| 函数 |   说明   |
| ---- | -------- |
| process | 取得url页面的文章内容，参数为url: str, time_out: int |

#### 示例

见anjuke.py

### 2.2 TO_BE_CONTINUE

#### 2.2.1 TO_BE_CONTINUE

```
TO_BE_CONTINUE
```


