# Linux 作业八：JobSpider

> 目标：
>
> 用Python或Java或C/C++等编写网络爬虫，获取1000条有Linux系统需求的招聘信息。（1）确定招聘网站及组织结构；（2）爬取职位介绍的url、职位名称、公司名称、城市、发布时间、职责描述等信息；（3）检索出“职责描述”中有“Linux”的招聘信息。

## Getting Started

```shell
git clone --depth=1 https://github.com/m8524769/JobSpider.git
cd ./JobSpider
pip3 install -r requirements.txt
scrapy crawl linux_job -o linux_jobs_zhipin.csv
```

## Usage

1.  自定义爬取数据条数：（默认为10条）

```shell
scrapy crawl linux_job -o linux_jobs_zhipin.csv -a count=100
```

2.  自定义导出格式：(默认为csv)

```shell
scrapy crawl linux_job -o linux_jobs_zhipin.json
```

## F.A.Q.

> 运行时出现`DNS lookup failed`咋办？

打开`/etc/hosts`并在最后添加新行：
```
60.205.129.48   www.zhipin.com
```

### JobSpider数据来源：[BOSS直聘](https://www.zhipin.com)

> [BOSS直聘-互联网招聘神器！](https://www.zhipin.com)
>
> BOSS直聘是权威领先的招聘网，开启人才网招聘求职新时代，让求职者与Boss直接开聊、加快面试、即时反馈，找工作就来BOSS直聘和Boss开聊吧！
