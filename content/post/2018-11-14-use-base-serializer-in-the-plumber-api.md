---
title: use `base::serializer()` in the plumber API
author: Xianying Tan
date: '2018-11-14'
slug: use-base-serializer-in-the-plumber-api
categories:
  - en
tags:
  - R
  - web
  - programming
  - sharing
  - tech
---

Recently, I need to share an R model on the server to my colleagues who use R. [Plumber](https://www.rplumber.io) comes to my mind immediately. Build a web API using plumber is really easy. I love the roxygen-way to define the API. It's elegant and easy to maintain.

Usually, web APIs use [JSON](http://json.org/) to represent data. Unfortunately, JSON encodes objects in a string, which may result in information losses. For example, the attributes (other than names) cannot be preserved. And it causes troubles:

- The user has to set back the attributes explicitly after the JSON results being parsed because there's no way to tell `["2018-11-15"]` is a string or a date in the pure JSON format. Or you have to store all the attributes in a seperate list, which is tedious and error-prone.

- Some issue is difficult to solve like you can't represent a zero-row dataframe in JSON (`jsonlite::toJSON(iris[0,])` returns `[]`). You have to deal with such corner cases by yourself.

- Parse a large R object to JSON can be quite slow[^1].

Luckily, all my "clients" (my colleagues) are R users, so I don't really need a general web API. JSON is only one of the many methods to [serialize](https://en.wikipedia.org/wiki/Serialization) objects and I'm not bound to it. Due to the existence of `base::saveRDS()`, I know there must be a serializing method provided by R itself - whether the method is exported or not is the only thing in doubt. Fortunately, with little effort, `base::serialize()` and `base::unserialize()` are the cures I'm looking for.

My solution is provided in the code below. Since the rds file is _almost_ the seamless representation of the R objects (external pointers are the exception), using `base::serialize()` as the customized serializer of the plumber API minimizes the efforts required to establish a stable plumber API for the R users.

Enjoy!

[^1]: Let's make a large double vector by `v <- rnorm(1e8)`, `system.time(invisible(jsonlite::toJSON(v)))` costs 27 seconds while `system.time(invisible(serialize(v, NULL)))` costs less than 4 seconds on my computer

## UPDATE @2020/03/21

As the time of writing, the dev version of `plumber` now gains the new native serializer `rds`.

---

## The sample code (BOTH POST and RETURN r objects)

- Place all the scripts under one same folder.
- Execute `main.R` to launch the API server.
- Execute `client.R` to test the API.

### plumber.R

```r
#* @post /api
#* @serializer rds
function(req) {
  req$robj
}
```

### main.R

(In practice, you probably want to have a condition inside. A good example is this: https://github.com/ozean12/protopretzel/blob/master/R/protobuf_filter.R)

```r
library(plumber)
x <- plumb("plumber.R")
x$filter("robj", function(req) {
  req$rook.input$rewind()
  req$robj <- unserialize(req$rook.input$read())
  plumber::forward()
})
x$run(debug = TRUE, port = 9999)
```

### client.R

```r
out <- httr::POST(
  "http://127.0.0.1:9999/api",
  encode = "raw",
  body = serialize(iris, NULL),
  httr::content_type("application/octet-stream")
)
# you may need to check httr::status_code() == 200L
# or if is.raw(httr::content(out)) is TRUE, first
base::unserialize(httr::content(out))
```
