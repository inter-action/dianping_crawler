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


## with Makefile:

    make run       # run this project.


# Neo4J

supported datatypes:
* Numeric values
* String values
* Boolean values
* Lists of any other type of value

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

        





























