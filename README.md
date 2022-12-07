[//]: использует все команды из docker-compose.yml и запускает их на переднем плане
docker-compose up

[//]: использует все команды из docker-compose.yml и запускает их на бэкграунде
docker-compose up -d --build

[//]: удалить предыдущие контейнеры
docker-compose down -v

[//]: 
docker-compose exec service* command* 

[//]:service* - сервисы из docker-compose.yml, например web
[//]:command* - комадна из сервиса
