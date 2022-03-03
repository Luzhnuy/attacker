<h1 align="center">Russian warship, go fuck yourself!</h1>
<p align="center">
   <a href="./README.md">Українське README</a> |
   <a href="./README_EN.md">English README</a>
</p>

## 🤔 Overview

- The repo contains [Python 3](https://python.org) [script](./attack.py), which uses russian proxies and retrieves list of sites to attack from our API which scanning bastards websites.
- ⚠ The script uses a proxy, but be careful, it is desirable to protect yourself with a VPN.

## 🚀 Quick start

### Windows

- Install [Python 3.8](https://python.org) (or later version)
  > ⚠ **IMPORTANT**: Make sure to select `Add Python to PATH` checkbox ([see screenshot](http://wind10.ru/wp-content/uploads/2020/02/pp_image_4620_v0cz5agbht0001_add_Python_to_Path.png))

- Clone repository:
  ```shell
  git clone https://github.com/Luzhnuy/attacker.git
  ```

- Run `install.bat` to install all the required dependencies

- Using terminal (command line or PowerShell) run the script:

  ```shell
  python attack.py
  ```

### Linux and MacOS

- Install [Python 3.8](https://python.org) (or later version)
  > ⚠ Linux users, your system may have Python version 2 pre-installed, which means that you need to run this program with the `python3` command and set the installation requirements with the `pip3` command.

- Clone repository:
  ```shell
  git clone https://github.com/Luzhnuy/attacker.git
  ```

- Install all the required dependencies:
  ```shell
  pip install -r requirements.txt
  ```

- Run the script:
  ```shell
  python attack.py
  ```

### Docker

- Install [Docker](https://docker.com):
  - Docker for Windows: https://ravesli.com/ustanovka-docker-v-windows/
  - Docker for MacOS: https://docs.docker.com/desktop/mac/install/
  - Linux: https://docs.docker.com/engine/install/

- Download docker image:

  ```shell
  docker pull ghcr.io/luzhnuy/attacker:latest
  ```

- Launch the container for the 500 threads:

  ```shell
  docker run --rm ghcr.io/luzhnuy/attacker:latest 500
  ```

### Docker Compose

`docker-compose` allows you to easily run containers in parallel without having to keep multiple terminals opened. To run on servers - perfect choice.

- Clone repository:
  ```shell
  git clone https://github.com/Luzhnuy/attacker.git
  ```

- Build and run `5` containers **in parallel** (each handles `500` connections):

  ```shell
  docker-compose up --build --scale attacker=5
  ```

- Stop containers from `docker-compose.yml` file: `Ctrl + C`

---

### For people who are not very familiar with computer science, Windows users

1. Download the archive https://drive.google.com/file/d/1aQR53fcbvkGY-bY0V4YhzLY6obh8H6Ln/view?usp=sharing

2. Extract archive
   > ⚠ **IMPORTANT**! DO NOT extract files to desktop folder and not to a folder contains cyrillic symbols. Preferred place to extract is the root of the drive `D:`

3. Find the `install.bat` file (you may see it as just `install`).
   
   Click on it using right-click, select `Start as Administrator`.

4. Follow step by step everything you see in the black window (press the number of the corresponding item, press Enter, allow programs to be installed, at the end select the next item.
   <i> For example "Install python (step1)" - You need to enter the number 1 and press enter </i>

5. When the process of installing everything you need is complete, a wizard will open in which you can run the Attack.bat file (maybe just Attack).

In the future, you no longer need to run install, just start `attack.bat` to get started. You also don't need to check for updates, this process happens automatically.

> ⚠ If you have already installed `bash` on your Windows machine - do not use` bash`, use `PowerShell` or` cmd`
