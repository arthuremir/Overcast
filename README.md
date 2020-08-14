Умный сервис прогноза погоды.

ПРИМЕР РАБОТЫ: https://overcast-ycloud-school.herokuapp.com

Выбранный уровень сложности - задание со звездочкой + интерактивная карта + график с прогнозом

Использованные языки программирования и технологии:
- Heroku
- Python, Flask, Gunicorn, Matplotlib
- HTML/CSS/JS
- OpenWeatherMapAPI (PyOWM)
- MapBoxAPI

Интерфейс представляет собой веб-сайт.

У пользователя есть два способа ввода информации.

1) Ввод на странице /forecast названия интересующей локации на английском языке.
(Пример - `Moscow`)
Есть возможность уточнить локацию, вписав после запятой название страны полностью
или ее двухбуквенный код (Пример - `Moscow, RU`).

2) Карта на основе MapBoxAPI (страница /map). Пользователь кликает на интересующее его место 
на карте, отправляет запрос и исходя из координат выбранной точки получает прогноз.

В случае, если данные введены корректно, пользователь получает в ответ текущую температуру,
иконку, отражающую текущую погоду, а также график с прогнозом температуры на следующие 5 дней 
(шаг - 3 часа), который открывается по кнопке `OPEN PLOT`, и простую рекомендацию по одежде. 
В случае, если запрос произведен до 21:00, рекомендация рассчитывается на основе прогнозов 
до 21:00 (включительно) текущего дня. В случае, если запрос отправлен позже 21:00, 
рекомендация рассчитывается на основе прогнозов на следующий день, начиная с 6:00. Рекомендация
использует среднюю температуру за расчетный промежуток. В случае, если хотя бы один раз за
промежуток прогнозируется дождь или изморось, будет рекомендовано взять с собой зонт.

Сервис использует обертку PyOWM над OpenWeatherMapAPI.
При нажатии на кнопку `Go` отправляется GET-запрос на сервер, который в свою очередь запрашивает
данные с OpenWeatherMap и возвращает пользователю, подставляя данные в HTML-шаблоны (Jinja2).

Запуск:
`git clone https://github.com/arthuremir/Overcast.git`
`cd Overcast`
`pip3 install -r requirements.txt`
`set FLASK_APP=start.py`
`flask run`

Возможные улучшения:
- кэширование
- автоматическое удаление графиков через 10 минут
