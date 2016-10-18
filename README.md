# About this Repo


# Project Settings Up

## Preliminaries:
install virtualenv, pip, ipython !


## 
* install ipython # REPL 很重要！
* setting up virtual env, & activate it 

        virtualenv .env 
        source .env/bin/activate  
        deactivate  # deactivate virtualenv
    
* install dependencies:

        # all installations goes to `./.env/lib/python3.5/site-packages`
        touch requirements.txt
        pip install NumPy
        pip install SciPy
        pip install -U scikit-learn

* working with pip:

        pip freeze > requirements.txt #freeze dependencies



* setting up Makefile
    
    http://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html
    https://gist.github.com/bsmith89/c6811893c1cbd2a72cc1d144a197bef2


## with Makefile:

    make run-main       # run this project.


## with vscode:
https://code.visualstudio.com/docs/languages/python

## with ipython
先activate virtualenv, then `>ipython`

    ctrl + l  #clear screen
    
    # --- auto reload module:
    # http://stackoverflow.com/questions/5364050/reloading-submodules-in-ipython

    %load_ext autoreload
    %autoreload 2

    


# Python3 language:
python3 module system - https://docs.python.org/3/tutorial/modules.html

    dir()               # print out what available in this module
    import builtins     # see what inside builtins
    

Exceptions - https://docs.python.org/3/tutorial/errors.html


# Neo4J


# Links

* [sklearn working with text example](http://scikit-learn.sourceforge.net/stable/auto_examples/index.html#working-with-text-documents)




## todos:

    done: 
        test using ipython with virtualenv activated

    pending:
        add a linter
        add flask, add restful webservices, 如果是练习的目的话，这个应该不需要了，再看
        add docker, then config Makefile again.
        ! learning more about ipython
        string format - http://www.python-course.eu/python3_formatted_output.php
        find a better way to handle __pycache__, generate it in non-src folder
        add python unit test

        





























