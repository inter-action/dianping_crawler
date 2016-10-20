# About this Repo
这个项目是用python+webdriver爬取大众点评网的用户数据(关系+评价)。然后存储到neo4j数据库中进行分析。
如果是其他网站, 你需要更改代码。

大众点评网有反扒策略,中间触发过几次(510条点评数据, 触发过), 目前代码中没有实现完备的解决方案。

性能效率的问题: 如果是510条数据, 爬虫加上sleep之后, 大概会20多分钟。这显然有些慢。这个
未来，可以把爬虫并发掉(这步需要和neo4j存储进行解耦).至于用多线程还是多进程的方式。这个需要以后
实验下，主要是不是特别清楚webdriver支不支持并发。然后将数据持久化到本地（目前使用python pickle lib）
,到存储neo4j时候, 从本地去load数据。 

对于存储到neo4j之后如何分析, 这个就不说了, 以后会放张存储到neo4j的截图。

# Project Settings Up

## Preliminaries - 前置条件:
* 你需要装chrome webdriver
* 你需要启动neo4j数据库.如果你用docker的话就执行:

    ```
    docker run \
        --publish=7474:7474 --publish=7687:7687 \
        --volume=$HOME/neo4j/data:/data \
        neo4j
    ```
* my python version - Python 3.5.2

## 启动

    pip install -r requirements.txt
    make run       # run this project.



## ---
* install ipython # REPL 很重要！
* setting up virtual env, & activate it 

        virtualenv .env 
        source .env/bin/activate  
        deactivate  # deactivate virtualenv
    
* install dependencies:

        pip install -r requirements.txt

* working with pip:

        pip freeze > requirements.txt #freeze dependencies


# Neo4J

supported datatypes:
* Numeric values
* String values
* Boolean values
* Lists of any other type of value

# ref docs:

* selenium - http://selenium-python.readthedocs.io/getting-started.html
* neo4j developer ref - http://neo4j.com/docs/developer-manual/current/introduction/
* tutorialspoint python - https://www.tutorialspoint.com/python/

# Links

* [sklearn working with text example](http://scikit-learn.sourceforge.net/stable/auto_examples/index.html#working-with-text-documents)



## todos:

    done: 
        add python unit test

    pending:
        add a linter
        在neo4j持久层方法上添加decorator, 抽离session.create, session.close语句
        添加并发?根据用户评论数量决定是否启用并发?-这个优先级不是很高
        将爬虫中sleep可配置
        add logger to replace print method

        





























