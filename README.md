# api_yamdb
www.danilalogunov.tk
### Описание
Данный проект является API для социальной сети Yatube.
### Технологии
Python 3.9
Django
Django Rest Framework
Nginx
### Запуск проекта
- Склонируйте проект
https://github.com/Kedow132/infra_sp2
коммандой в терминале
git clone https://github.com/Kedow132/infra_sp2
- В корневой папке проекта в терминале выполните комманду:
docker-compose up
Проект станет доступен по адресу
localhost
### Настройка проекта
- Когда проект запущен, следует сделать миграции коммандой в терминале:
docker-compose exec web python manage.py migrate --noinput
- Чтобы создать суперпользователя (админа), используйте комманду:
docker-compose exec web python manage.py createsuperuser
Следуйте инструкциям
- Следует собрать статические файлы проекта
docker-compose exec web python manage.py collectstatic --no-input
- Чтобы добавить тестовые данные в БД используйте комманду
docker-compose exec web python manage.py loaddata fixtures.json
### Полезные комманды
- Чтобы остановить проект используйте комманду
docker-compose down



https://github.com/Kedow132/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg
