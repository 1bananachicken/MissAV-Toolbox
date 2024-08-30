# MissAV封面下载器
### 安装
在Release中下载`missav_utils-0.2-py3-none-any.whl`文件，然后在命令行中执行以下命令：
```shell
pip install missav_utils-0.2-py3-none-any.whl
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

#### 初始化参数
movie_type: enum
```
MovieType.professional  # 有码
MovieType.fc2           # FC2
```
sort_by: enum
```
SortBy.ReleaseDate      # 发行日期
SortBy.RecentUpdate     # 最近更新
SortBy.TodayViews       # 今日观看
SortBy.WeeklyViews      # 本周观看
SortBy.MonthlyViews     # 本月观看
```

#### 示例
下载今日观看前十的有码电影封面
```python
from missav_utils.MissavCovers import CoverDownloader, MovieType, SortBy

downloader = CoverDownloader(movie_type=MovieType.professional, sort_by=SortBy.TodayViews)
downloader.download()
```
### 效果
<details>
<summary>⚠️⚠️⚠️NSFW警告！！！⚠️⚠️⚠️</summary>

<img src="./intro/fig1.png" width=50%>

</details>
