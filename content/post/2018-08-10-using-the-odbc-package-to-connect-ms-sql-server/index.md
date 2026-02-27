---
title: 在Linux下使用odbc包连接MSSQL Server
author: 谭显英
date: '2018-08-10'
slug: using-the-odbc-package-to-connect-ms-sql-server
originalLang: zh
categories:
tags:
  - R
  - odbc
  - encoding
  - FreeTDS
  - unixODBC
  - MSSQLServer
  - programming
  - tech
  - note
  - sharing
---

在[《忍无可忍的Encoding》](/post/2018/05/07/cant-bear-with-encoding-any-longer/)一文中提到：

> [RSQLServer包](https://github.com/imanuelcostigan/RSQLServer)退役了，作者建议使用[r-dbi/odbc包](https://github.com/r-dbi/odbc)代替。但是，odbc包并没有像RODBC包一样（版本1.1.6已经修复这个问题），_预先把SQL字符编码转换成和数据库一致的字符编码_ ，导致无法正确执行包含中文的SQL语句（如果该语句的字符编码和数据库的编码不一致）。

举个栗子：

1. MSSQL Server数据库：一般放在某个中文Windows Server服务器上，大概率其数据库默认字符编码是GB2312;
1. 客户端：使用某个中文的Windows（默认字符编码也是GB2312）；
1. 建立一个使用odbc包的数据库链接`conn`，执行下列语句：

    ```r
    sql_native <- "select * from tbl where field_a = '中文'"
    sql_utf8 <- enc2utf8(sql_native)
    DBI::dbGetQuery(conn, sql_native)
    # 会有数据
    DBI::dbGetQuery(conn, sql_utf8)
    # 要么报错要么返回一个空的数据集
    ```

我提交了这个八阿哥的报告[r-dbi/odbc#179](https://github.com/r-dbi/odbc/issues/179)，作者[Jim Hester](https://github.com/jimhester) 也很快地解决了这个问题，测试了下没问题，一切看起来似乎很美好。

今天正好有空，决定正式把所有和RSQLServer相关的数据链接都使用odbc替换掉（只需要把负责数据库连接的包进行修改，然后重新测试部署即可）。Windows上一切正常，但是在Linux中又遇到了问题 —— 只要是包含中文的SQL都会报错：`Invalid multibyte sequence`。

鼓捣了一会儿后意识到，在Linux下使用的是FreeTDS驱动（unixODBC只是一个驱动管理器，不同的数据库还需要装不同的驱动才行），但和微软的SQL Server驱动不同，FreeTDS默认会将返回的数据结果字符部分转换为UTF8编码，然而odbc包却假设数据库返回结果的编码和数据库编码一致，而且会在结果返回到R之前，试图将数据库编码转换为标准的UTF-8编码 —— 于是便导致了“试图将已经是UTF8编码的数据当做是GB2312重新转换为UTF8而报错”的问题（相信我，这句子多读几遍就能读顺 :smiley: ）。

知道了病因，医生开药便简单了，简单搜索了下便知晓了FreeTDS可以在连接中设置`clientcharset`这个参数，配置成GB2312便可以保证其返回的数据结果和odbc包期待的结果一样啦。

简单总结下“在Linux下使用odbc包连接MSSQL Server”的注意事项：

1. 安装unixODBC(驱动管理器)和FreeTDS(MSSQL Server驱动)；

    ```bash
    apt-get install unixodbc unixodbc-dev tdsodbc
    ```
    
1. 注册FreeTDS驱动，可参照[《Linux下连接MS Sql server -- 使用ODBC/FreeTDS组合(详细)》](http://www.cnblogs.com/lexus/archive/2012/09/26/2704382.html)或者我的[Docker文件](https://github.com/shrektan/rdocker/blob/d232bcc43b14942e569684c4b73f9c8915ea0997/rdocker4working/Dockerfile#L69)，总之就是让unixODBC知道你的Driver文件libtdsodbc.so在哪里；
    
    - 把下面的文本保存在任意地方，比如`/var/tds.driver.template`，注意Driver的地址可能未必和我的一致；
    ```
    [FreeTDS]
    Description = Free TDS
    Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
    ```
    
    - 然后执行下面的语句即可。
    ```bash
    odbcinst -i -d -f /var/tds.driver.template
    ```

1. 按如下方式配置你的odbc链接。

    ```r
    conn <- DBI::dbConnect(
      drv = odbc::odbc() ,
      server = "your ip",
      port = 1433, # FreeTDS必须要填端口号
      database = "your db",
      uid = "your user name",
      pwd = "your password",
      encoding = "GB2312", # 服务器编码-中文一般就是这个
      driver = "FreeTDS", # 和第二步你设置的名称一样就好
      clientcharset = "GB2312" # 必须要加这一个参数
    )
    ```


最后，想起益辉大人提到，写文章[“最重要的因素还是胸中是否有一股不吐不快的气”](https://yihui.org/cn/2018/07/fluent-essay/)。这股“不吐不快的气”我自己是时常都能感觉到的（我可是个吐槽大王啊），可惜经常没能及时将这股气幻化为文字，一拖便散了，不想写了。不过最近积攒的能量（:u6709:怨气:stuck_out_tongue_closed_eyes:	）尤为多，且看能吐多少。
