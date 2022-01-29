# discord_yandex_music_bot

Короче это демка музыкального дискорд бота который работает напрямую с яндекс музыкой (спасибо [MarshalX](https://github.com/MarshalX) за API).


Чтобы все работало:

- 1 - идем на https://ffmpeg.org/download.html и скачиваем `Windows builds from gyan.dev`
оттуда нам нужны 3 файла __ffmpeg.exe ffplay.exe ffprobe.exe__. Кидаем их в папку с кодом
- 2 - устанавливаете `requirements.txt` 
- 3 - в файле `dic-part.py` в самом низу вписываете свой токен
- 4 - в `y_musick_start.py` в 7 строчке прописываете свои данные(проверьте в настройках яндекс акка чтобы была авторизация по логину\паролю а не как-то иначе)

Запускать нужно `dic-part.py` (через idle или консоль как удобнее)



API ЯМ выплёвывает дофига ошибок в консоль, что в целом ни на что не влияет. Если будет желание их убрать - идете в папку с библиотекой,
по варнингу ищете файл(ну или тупо перебором) и комментируете строки на подобии
```python
super().handle_unknown_kwargs(self, **kwargs)
```
(подробнее по теме читайте тут -> [тык](https://docs.python.org/2/library/warnings.html#temporary-suppressing-warnings))


префикс "!"(меняется на свой в 302 строчке в `dic-part.py`)

Функционал:

-  `play (текст)` - добавить песню по названию\автору или все вместе
-  `queue` - отобразить текущую очередь
-  `stop` - ливает с канала 
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


