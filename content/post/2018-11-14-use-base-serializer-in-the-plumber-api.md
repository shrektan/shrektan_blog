---
title: use `base::serializer()` in the plumber API
author: Xianying Tan
date: '2018-11-14'
slug: use-base-serializer-in-the-plumber-api
categories:
  - programming
  - sharing
  - tech
tags:
  - R
  - web
---

Recently, I need to share an R model on the server to my colleagues who use R. [Plumber](https://www.rplumber.io) comes to my mind immediately. Build a web API using plumber is really easy. I love the roxygen-way to define the API. It's elegant and easy to maintain.

Usually, web APIs use [JSON](http://json.org/) to represent data. Unfortunately, JSON encodes objects in a string, which may cause information losses. For example, the attributes (other than names) cannot be preserved. It causes troubles: 

- The user has to set back the attributes explicitly after the JSON results being parsed because there's no way to tell `["2018-11-15"]` is a string or a date in the pure JSON format. Or you have to store all the attributes in a seperate list, which is tedious and error-prone.

- Some issue is difficult to solve like you can't represent a zero-row dataframe in JSON (`jsonlite::toJSON(iris[0,])` returns `[]`). You have to deal with such corner cases by yourself.

Luckily, all my "clients" (my colleagues) are R users, so I don't really need a general web API. JSON is only one of the many methods to [serialize](https://en.wikipedia.org/wiki/Serialization) objects and I'm not bound to it. Due to the existence of `base::saveRDS()`, I know there must be a serializing method provided by R itself - whether the method is exported or not is the only thing in doubt. Fortunately, with little effort, `base::serialize()` and `base::unserialize()` are the cures I'm looking for.

My solution is provided in the code below. Since the rds file is _almost_ the seamless representation of the R objects (external pointers are the exception), using `base::serialize()` as the customized serializer of the plumber API minimizes the efforts required to establish a stable plumber API for the R users.

Enjoy!

### Add the customized erializer first

```r
plumber::addSerializer("r_obj_serializer", function() {
  function(val, req, res, errorHandler) {
    tryCatch({
      res$setHeader("Content-Type", "application/octet-stream")
      res$body <- base::serialize(val, NULL, ascii = FALSE)
      return(res$toResponse())
    }, error = function(e) {
      errorHandler(req, res, e)
    })
  }
})
```

### Use the customized serializer in the plumber file

```r
#* @post /api
#* @serializer r_obj_serializer
function() {
  ...
}
```

### Get the API results

```r
out <- httr::POST(
  url,
  encode = "raw",
  body = body,
  httr::content_type("application/octet-stream"),
  ...
)
# you may need to check httr::status_code() == 200L 
# or if is.raw(httr::content(out)) is TRUE, first
base::unserialize(httr::content(out))
```
