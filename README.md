# discord_yandex_music_bot

Короче это демка музыкального дискорд бота который работает напрямую с яндекс музыкой (спасибо [MarshalX](https://github.com/MarshalX) за API).


Чтобы все работало, очевидно нужен python3.6+ а также:

- 1 - идем на https://ffmpeg.org/download.html и скачиваем `Windows builds from gyan.dev`
оттуда нам нужны 3 файла __ffmpeg.exe ffplay.exe ffprobe.exe__. Кидаем их в папку с кодом
- 2 - устанавливаете `requirements.txt` (cd <путь до папки с кодом> <Enter> pip install -r requirements.txt <Enter>) если не знаете что это, прочитайте тут -> [requirements.txt](https://semakin.dev/2020/04/requirements_txt/)
- 3 - в файле `dic-part.py` в самом низу вписываете свой токен
    - 3.1 Откуда взять токен?
      - идем на https://discord.com/developers/applications, авторизуемся и все дела
      - на вкладке Applications в правом верхнем углу нажимаем `New Application`
      - заполняем имя и попадаем на страницу с информацией о приложении (можете менять имя, описание, ставить иконку но это пока не важно)
      - нам нужно перейти во вкладку `Bot` по кнопке в правой понели
      - нажимаем `Add bot`, соглашаемся со всем
      - мотаем страницу вниз до `Bot Permissions`. Ставим галочку у _Administrator_ и сохраняем(в дальнейшем можете настроить только на возможность говорить, писать и читать)
      - мотаем в самый верх, под названием бота тыкаем по кнопке `Copy`, соответсвенно копируем токен
    - 3.2 Как пригласить бота на сервер?
      - нам понадобится данная ссылка: https://discordapp.com/oauth2/authorize?&client_id=`APPLICATION_ID`&scope=bot&permissions=0 где `APPLICATION_ID` надо заменить на свой
      - APPLICATION_ID находится на вкладке `General Information` под строкой _tags_ вашего приложения на портале разработчиков


Запускать нужно `dic-part.py` (через idle или консоль как удобнее)
(через консоль:
- cd <путь до папки с кодом>
- python dic-part.py)
p.s. не забудьте авторизоваться в консоли при первом запуске

API ЯМ выплёвывает дофига ошибок в консоль, что в целом ни на что не влияет. Если будет желание их убрать - идете в папку с библиотекой,
по варнингу ищете файл(ну или тупо перебором) и комментируете строки на подобии
```python
super().handle_unknown_kwargs(self, **kwargs)
```
(подробнее по теме читайте тут -> [тык](https://docs.python.org/2/library/warnings.html#temporary-suppressing-warnings))


префикс "!"(меняется на свой в 302 строчке в `dic-part.py`)

Функционал:

-  `play (текст)` - добавить песню по названию\автору или по ссылке на альбом (пример: https://music.yandex.ru/album/4784938)
-  `queue` - отобразить текущую очередь
-  `stop` - ливает с канала 
-  `clear` - очистка очереди
-  `show_playlists` - отобразить названия ваших плейлистов в ЯМ 
-  `playlist (текст)` - добавить в очередь плейлист по названию !ЕСЛИ В ПЛЕЙЛИСТЕ МНОГО ТРЕКОВ НАДО ПОДОЖДАТЬ! 
-  `shuffle` - перемешать очередь  
-  `skip` - следующий трек 
-  `pause` - пауза  
-  `resume` - продолжить 
-  `new_channel (текст)` - перейти в другой войс канал (указать название)  
-  `volume (цифра)` - по логике должен регулировать громкость, но я чет не заметил чтобы работало
  
  
Пожалуйста, если вы нашли новую ошибку, скопируйте консольный лог и отправьте мне в [Issues](https://github.com/senaKash/discord_yandex_music_bot/issues)
или [Telegram](https://t.me/MikuON)


