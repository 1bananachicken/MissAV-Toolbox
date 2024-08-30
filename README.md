# MissAV封面下载器
### 安装
在Release中下载`missav_utils-0.1-py3-none-any.whl`文件，然后在命令行中执行以下命令：
```shell
pip install missav_utils-0.1-py3-none-any.whl
```

### 使用
#### 配置代理

如果使用的clash默认设置，请在系统环境变量中添加`http_proxy`和`https_proxy`两个变量，值为`http://127.0.0.1:7890`

或者添加以下内容
```python
import os
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
```

#### 基础用法
```python
from missav_utils.MissavCovers import CoverDownloader

downloader = CoverDownloader()
downloader.download()
```


### 效果
<details>
<summary>⚠️⚠️⚠️NSFW警告！！！⚠️⚠️⚠️</summary>

<img src="./intro/fig1.png" width=50%>

</details>
