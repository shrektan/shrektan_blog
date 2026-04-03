---
title: Using the odbc Package to Connect to MSSQL Server on Linux
author: Xianying Tan
date: '2018-08-10'
slug: using-the-odbc-package-to-connect-ms-sql-server
originalLang: zh
categories:
  - 技术
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

As I mentioned in [*Can't Bear with Encoding Any Longer*](/post/2018/05/07/cant-bear-with-encoding-any-longer/):

> The [RSQLServer package](https://github.com/imanuelcostigan/RSQLServer) has been retired, and its author recommends using the [r-dbi/odbc package](https://github.com/r-dbi/odbc) as a replacement. However, unlike the RODBC package (which fixed this issue in version 1.1.6), the odbc package does not _convert the SQL string encoding to match the database's encoding beforehand_, making it unable to correctly execute SQL statements containing Chinese characters (if the encoding of the statement differs from the database encoding).

Here's an example:

1. MSSQL Server database: typically hosted on a Chinese Windows Server, where the default database encoding is most likely GB2312;
1. Client: running on a Chinese Windows machine (also defaulting to GB2312 encoding);
1. Create a database connection `conn` using the odbc package and execute the following:

    ```r
    sql_native <- "select * from tbl where field_a = '中文'"
    sql_utf8 <- enc2utf8(sql_native)
    DBI::dbGetQuery(conn, sql_native)
    # Returns data
    DBI::dbGetQuery(conn, sql_utf8)
    # Either throws an error or returns an empty dataset
    ```

I filed a bug report at [r-dbi/odbc#179](https://github.com/r-dbi/odbc/issues/179), and the author [Jim Hester](https://github.com/jimhester) quickly resolved the issue. After testing, everything seemed to work perfectly fine.

Today I finally had some free time and decided to officially replace all RSQLServer-based database connections with odbc (all I needed to do was modify the package responsible for database connections and then re-test and deploy). Everything worked smoothly on Windows, but on Linux I ran into another problem -- any SQL containing Chinese characters would fail with: `Invalid multibyte sequence`.

After some tinkering, I realized that on Linux, the FreeTDS driver is used (unixODBC is just a driver manager; you still need to install separate drivers for different databases). Unlike Microsoft's SQL Server driver, FreeTDS converts the character portion of returned data to UTF-8 encoding by default. However, the odbc package assumes that the encoding of the returned data matches the database encoding, and it attempts to convert the data from the database encoding to standard UTF-8 before returning results to R. This leads to the problem of "trying to re-convert data that is already UTF-8 by treating it as GB2312" (trust me, read that sentence a few more times and it'll make sense).

Once the root cause was identified, the fix was straightforward. A quick search revealed that FreeTDS allows setting the `clientcharset` parameter in the connection. By setting it to GB2312, the returned data will match what the odbc package expects.

Here's a brief summary of things to keep in mind when using the odbc package to connect to MSSQL Server on Linux:

1. Install unixODBC (driver manager) and FreeTDS (MSSQL Server driver):

    ```bash
    apt-get install unixodbc unixodbc-dev tdsodbc
    ```

1. Register the FreeTDS driver. You can refer to [this guide on connecting to MS SQL Server on Linux using ODBC/FreeTDS](http://www.cnblogs.com/lexus/archive/2012/09/26/2704382.html) or my [Dockerfile](https://github.com/shrektan/rdocker/blob/d232bcc43b14942e569684c4b73f9c8915ea0997/rdocker4working/Dockerfile#L69). The point is to let unixODBC know where your driver file libtdsodbc.so is located.

    - Save the following text anywhere, for example `/var/tds.driver.template` (note that the Driver path may differ on your system):
    ```
    [FreeTDS]
    Description = Free TDS
    Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
    ```

    - Then run the following command:
    ```bash
    odbcinst -i -d -f /var/tds.driver.template
    ```

1. Configure your odbc connection as follows:

    ```r
    conn <- DBI::dbConnect(
      drv = odbc::odbc() ,
      server = "your ip",
      port = 1433, # FreeTDS requires the port number
      database = "your db",
      uid = "your user name",
      pwd = "your password",
      encoding = "GB2312", # Server encoding - typically this for Chinese
      driver = "FreeTDS", # Must match the name you set in step 2
      clientcharset = "GB2312" # This parameter is essential
    )
    ```


Finally, I recall Yihui once mentioned that the most important factor in writing is whether you have ["an urge that you simply can't hold back"](https://yihui.org/cn/2018/07/fluent-essay/). I feel this urge quite often (I'm quite the complainer, after all), but unfortunately I often fail to capture it in writing in time -- once I procrastinate, the momentum fades and I no longer feel like writing. That said, I've been accumulating a lot of energy (read: grievances) lately, so let's see how much I can get out.
