<h1 align="center">Russian warship, go fuck yourself!</h1>
<p align="center">
   <a href="./README.md">Українське README</a> |
   <a href="./README_EN.md">English README</a>
</p>

## 🤔 Що це?

- В репі лежить [Python 3](https://python.org) скрипт, який використовуючи російські проксі проводить навантажувальне тестування вебресурсів, використовуючи API.
- ⚠ Скрипт використовує проксі, але будьте обережні, бажано використовувати VPN.

## 🚀 Швидкий старт

### Windows 

- Ставимо [Python 3.8](https://python.org) або новіший ([інструкція](https://python-scripts.com/install-python-windows))
  > ⚠ Обов'язково ставимо галочку навпроти `Add Python to PATH` ([скриншот](http://wind10.ru/wp-content/uploads/2020/02/pp_image_4620_v0cz5agbht0001_add_Python_to_Path.png))

- Зтягуємо репу:
  ```shell
  git clone https://github.com/Luzhnuy/attacker.git
  ```

- Запускаємо `install.bat` щоб встановити всі необхідні депенденсі

- Через термінал (командну строку чи PowerShell) запускаємо скрипт:
  ```shell
  python attack.py
  ```

### Linux та MacOS

- Ставимо [Python 3.8](https://python.org) або новіший
  > ⚠ В Linux ваша система може мати попередньо встановлений Python версії 2, і це означає, що вам потрібно запустити цю програму за допомогою команди `python3` і встановити вимоги до встановлення за допомогою команди `pip3`

- Клонуємо репу:
  ```shell
  git clone https://github.com/Luzhnuy/attacker.git
  ```

- Встановлюємо всі необхідні депенденсі:
  ```shell
  pip install -r requirements.txt
  ```

- Запускаємо скрипт:
  ```shell
  python attack.py
  ```

### Docker
- Ставимо [Docker](https://docker.com): 
  - Docker for Windows: https://ravesli.com/ustanovka-docker-v-windows/
  - Docker for MacOS: https://docs.docker.com/desktop/mac/install/
  - Linux: https://docs.docker.com/engine/install/

- Завантажуємо докер імейдж:

  ```shell
  docker pull ghcr.io/luzhnuy/attacker:latest
  ```

- Запускаємо контейнер для 500 тредів:

  ```shell
  docker run --rm ghcr.io/luzhnuy/attacker:latest 500
  ```

#### Список змінних середовища Docker

- `ATTACKER_THREADS`: _(integer)_ Визначає кількість потоків, використаних у скрипті.
- `ATTACKER_TARGET`: _(JSON масив з URL-адресами)_ Визначає цільові сайти, які використовуватимуться як цілі замість динамічного списку сайтів, отриманих за допомогою API.

### Docker Compose

`docker-compose` дозволяє легко запускати контейнери паралельно без необхідності тримати відкритими декілька терміналів. Для запуску на серверах - саме те що треба.

- Клонуємо репу:

  ```shell
  git clone https://github.com/Luzhnuy/attacker.git
  ```

- Збираємо та запускаємо **паралельно** `5` контейнерів (по `500` коннектів на кожному):

  ```shell
  docker-compose up --build --scale attacker=5
  ```

- Зупинити всі контейнери з компоуз файлу: <kbd>Ctrl + C</kbd>

---

### Для людей, не дуже обізнаних в інформатиці, користувачів Windows

1. Завантажте архів https://drive.google.com/file/d/1aQR53fcbvkGY-bY0V4YhzLY6obh8H6Ln/view?usp=sharing

2. Розархівуйте кудись.
   > ⚠ ВАЖЛИВО! НЕ на робочий стіл, та не в папку з іменем кирилицею, краще всього в корінь диску `D:` скажімо.

3. Знайдіть файл `install.bat` (можливо він буде у вас відображатися як просто install).
   
   Відмітьте його та натиснувши праву кнопку мишки на ньому, виберіть з меню `Запустить от Администратора`.

4. Виконайте по черзі крок за кроком все, що побачите в чорному вікні (натисніть цифру відповідного пункту, нажміть <kbd>Enter</kbd>, дозвольте програмам встановитися, по закінченню оберіть наступний пункт.
   <i>Наприклад "Встановити python (step1)" - Вам потрібно ввести цифру `1` та натиснути <kbd>Enter</kbd></i>

5. Коли процес встановлення всього потрібного буде закінчено, відкриється провідник, в якому ви можете запустити файл `Attack.bat` (можливо буде просто Attack).

В майбутньому, не потрібно більше запускати install, для початку роботи достатньо запускати хіба `Attack.bat`. Також не треба перевіряти оновлення, цей процес відбувається автоматично.

> ⚠ Якщо ви вже встановили `bash` на своїй машині з Windows - не використовуйте `bash`, використовуйте `PowerShell` або `cmd`.
