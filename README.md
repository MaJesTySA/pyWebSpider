> 记录学习爬虫的过程，主要参考崔庆才大神的视频和书籍、慕课网课程，自己做了点更改。

# 爬取猫眼电影Top100

使用`requests库`和`regex`爬取猫眼电影Top100，保存为`csv`文件。

[MaoyanTop100](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/MaoyanTop100/MaoyanTop100.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/maoyantop100_1.png" width=50%/></div>
<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/maoyantop100_2.png" width=80% /></div>

# 爬取头条美图

使用`requests库`+`regex`+`BeautifulSoup`爬取头条美图，保存到`MongoDB`并下载图片文件。

[TouTiaoMeiTu](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/ToutiaoJiePai/TouTiaoMeiTu.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/toutiao_0.png" width=30%/></div>
<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/toutiao_1.png" width=50%</img></div>
<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/toutiao_2.png" width=50% ></div>

# 爬取京东美食

使用`selenium`+`PyQuery`爬取京东美食，保存到`MongoDB`。

[JDMeiShi](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/JingDongMeiShi/JDMeiShi.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/jdmeishi1.png" width=65% /></div>
<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/jdmeishi_2.png" /></div>

# 爬取微信文章

使用`ProxyPool`和`requests`+`pyQuery`爬取微信文章，保存到`MongoDB`。

[WeChatArticles](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/WeChatArticles/spider.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/wechat1.png" width=60% /></div>
<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/wechat2.png" width=60% /></div>

# 爬取知乎用户信息

使用`scrapy`爬取知乎用户信息，保存到`MongoDB`。

[zhihu](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/zhuhuUser/zhuhuUser/spiders/zhihu.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/zhihu_0.png" width=50%/></div>

# 爬取豆瓣书单信息

想看看甲骨文书系和汗青堂书系的信息，自己用`scrapy`写了个爬虫，保存到`MongoDB`。

[book_list_spider](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/DouBanBookList/DouBanBookList/spiders/book_list_spider.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/hanqingtang.png" /></div>

# 爬取微博搜索

使用`scrapy`爬取微博搜索页，需要N个账号，没做测试。

[weibo](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/WeiBoSearch/WeiBoSearch/spiders/weibo.py)

# 爬取技术博客文章

使用`scrapy`爬取CNBlogs最新文章，保存到`MongoDB`。

[cnblogs](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/CNBlogs_Articles/CNBlogs_Articles/spiders/cnblogs.py)

<div align=center><img src="https://github.com/MaJesTySA/pyWebSpider/raw/master/imgs/cnblogs_1.png" /></div>
<div align=center><img src="https://github.com/MaJesTySA/pyWebSpider/raw/master/imgs/cnblogs_2.png" /></div>

# 爬取技术博客新闻

使用`scrapy.ItemLoader`爬取CNBlogs新闻，并存入`MySQL`，比上一个更加简洁高效。

[cnblogs](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/CNBlogs_New/CNBlogs_imooc_ver/spiders/cnblogs.py)

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/cnblogsnew.png" /></div>

# 爬取知乎问答

还是使用`scrapy`框架，配合`selenium`和`chrome -remote--debugging`模式（知乎能够识别`ChromeDriver`）。

[zhihu](https://github.com/MaJesTySA/pyWebSpider/blob/master/src/zhihuAnswer/zhihuAnswer/spiders/zhihu.py)

**主要技术点**：

- [者也](https://github.com/996refuse/zheye)识别知乎倒立中文验证码。
- 使用[云打码](http://www.yundama.com/)识别英文验证码。

**问题列表**：

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/zhihuans_1.png" /></div>
**回答列表**：

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/zhihuans_2.png" width=80%/></div>
暂时没处理防爬（同一个Cookie同一时间多次访问）。

# 爬取拉勾网职位

使用`scrapy.CrawlSpider`爬取拉勾网职位。

<div align=center><img src="https://raw.githubusercontent.com/MaJesTySA/pyWebSpider/master/imgs/lagou.png" width=90%/></div>

