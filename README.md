# Сервис для транскрибации аудио файлов

Проект Умный диктофон

Сервис работает в связке с очередью RabbitMQ.

Алгоритм запуска:

1. Скачать проект
``` bash
git clone
```
2. Перейти в проект
``` bash
cd voice-recorder-ml-service
```
3. Собрать Docker image
``` bash
docker build -t voice-recorder-ml-service . 
```
4. Образ создан. Запускаем общий docker-compose файл с бекендом проекта. Обязательно в docker-compose должен быть RabbitMQ

Для production версии в ```data.config.py``` вынести логику использования переменных извне.