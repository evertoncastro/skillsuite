# Skill Suite Test


#### Virtual env
```
pip install virtualenv
virtualenv env
source env/bin/activate
```

#### Install packages
```
pip install -r src/requirements.txt
```

### Variables setup
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export FLASK_ENV=development
export FLASK_APP=src/main.py
```

#### Database setup
```
flask db init --directory=development_migrations
flask db migrate --directory=development_migrations
flask db upgrade --directory=development_migrations
```

### Renning tests
```
python tests/runner.py
```

### Start app
```
flask run
```
