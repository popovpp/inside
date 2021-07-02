Тестовое задание от компании Инсайд.

Репозиторий проекта можно склонировать по ссылке https://github.com/popovpp/inside.git
Запуск проекта осуществляется с использование docker-compose. На момент написания данного документа автор использовал версию 3. Версия Docker 19.03.14.

Перед запуском нужно провести миграции (команды запускаем в корневой папке проекта, где раположен файл docker-compose.yml):
docker-compose run web python manage.py makemigrations,
docker-compose run web python manage.py migrate.
Затем необходимо создать superuser:
docker-compose run web python manage.py superuser.
В корневой папке проекта запускаем:
docker-compose up.
Затем в адресной строке браузера вводим адрес:
http://0.0.0.0:8000/admin/
Средствами админки создаем еще минимум одного пользователя.
Затем открываем в браузере адрес http://0.0.0.0:8000/chat/client/
Это клиент, который сразу подключается к чату и может принимать сообщения зарегистрироавнных в чате пользователей.
В приложении создан API point для получения jwt token:
http://0.0.0.0:8000/auth-jwt/
Но для разнообразия сделал аутентификацию пользователя и выдачу токена во view.
Для демонстрации всех фич необходимо запустить второй браузер или открыть новую вкладку в текущем. 

Откройте любой другой браузер или новую вкладку в текущем браузере и также перейдите по адресу 
http://0.0.0.0:8000/chat/client/

В первом браузере введите имя пользователя и пароль (пользватель должен быть зарегистрирован в базе, см. текст выше) в верхние поля ввода и нажмите кнопку "Authorize".
Если имя м пароль валидные, то ниже кнопок выведется строка токена (это сделано только для иллюстрации).
Теперь в нижнем ряду нажмите кнопку "Send token" и почти сразу в большом текстовом поле высветится сообщение: "username: can send message". Теперь клиент может отправлять сообщения и запрашивать историю сообщений в базе.
В нижнем поле "Message" введите сообщение и нажмите кнопку "Send message". В большом текстовом поле вы увидите свое сообщение. Посмотрите большое текстовое поле другого клиента, которого вы подключили к чату в другом браузере, вы также увидите свое сообщение.
Попробуйте отправить сообщения с неавторизованного клиента (другой браузер), повторив действия, описанные выше. В большом текстовом поле вы увидите сообщение "chat_room: can't send message". 
Проведите операции авторизации на неавторизованном клиенте, повторив действия, описанные выше, после чего повторите отправку сообщения. В большом текстовом поле вы увидите свое сообщение. Посмотрите большое текстовое поле первого клиента, вы также увидите свое сообщение.
Для запроса исторических сообщений на авторизованном клиенте отправьте сообщение вида "history N", где N - это целое число, указывающее, сколько последних сообщений записанных в базу вы хотите получить. Количество пробелов между "history" и N должно быть не меньше одного. После отправки сообщения в большом текстовом поле вы увидите список пришедших сообщений вида:
admin: test
admin: rewert
admin: fresa
test: DRUZHBA
При потере соединения повторите операции авторизации.
