<h1>Docker</h1>
Создать образы и контейнеры DOCKER с помощью команд: "docker-compose build" и "docker-compose up".
<br>
<h2>Запуск</h2>
$ git clone git@github.com:Hoodnika/DRF_Django_project.git<br>

Создайте и заполните файл .env в корневой директории по подобию .env.sample:<br>

$ pip install -r requirements.txt <br>
$ python3 manage.py migrate $$ python3 manage.py runserver<br>
$ celery -A config worker --beat --scheduler django --loglevel=info<br>

Теперь проект готов работать, зарегистрируйтесь в приложении<br>
Если хотите создать admin в вашем приложении используйте команду :<br>
$ python3 manage.py createsuper

