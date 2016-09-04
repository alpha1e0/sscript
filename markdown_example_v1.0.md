

# 1 Markdown 语法示例


## 1.1 标题

标题用#号开头即可，1个#号是一级标题，2个##号是二级标题，依次类推


## 1.2 引用

> 这是个引用

> 一级引用
>> 二级引用（pandoc语法支持）


## 1.3 区块代码

	grep -r "test" ./*


## 1.4 段落

这是段落1

这是段落2，中间隔一个空行就可以了

正常文字

*斜体加重1*

**斜体加重2**

`高亮文字`


## 1.5 列表

* 项目1
* 项目2
* 项目3

1. the first one
2. the second one


## 1.6 代码

```{.python .numberLines startFrom="100"}
def foo():
    print "hello world"
```

反引号包含的内容表示HTML代码

`<h2>2号标题</h2>`


## 1.7 分割线

---


## 1.8 链接

### 1.8.1 行内链接

Google搜索: [Google一下](www.google.com)

My email is: [email](mailto:shiyan@h3c.com)

![双鱼座](/Users/apple/Pictures/avatar/双鱼座.jpg "双鱼座")

### 1.8.2 参考链接

I get 10 times more traffic from [Google][1] than from
[Yahoo][2] or [MSN][3].



[1]: http://google.com/ "Google"
[2]: http://search.yahoo.com/ "Yahoo Search"
[3]: http://search.msn.com/ "MSN Search"