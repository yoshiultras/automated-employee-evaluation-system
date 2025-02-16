# Automated Employee Evaluation System - API

Этот репозиторий содержит API для системы автоматизированной оценки сотрудников. Ниже приведена инструкция по запуску проекта.

## Требования

Для запуска проекта необходимо установить следующие компоненты:

- [Python](https://www.python.org/downloads/) (версия 3.8 или выше)
- [Git](https://git-scm.com/)



1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/automated-employee-evaluation-system/api.git

2. **Создайте виртуальное окружение**:
    ```bash
    python -m venv venv
    ```

3. **Активируйте виртуальное окружение**:

    На Windows:

    ```bash
    venv\Scripts\activate 
    ```
    На macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

4. **Установите зависимости**:

    ```bash
    pip install -r requirements.txt
    ```
5. **Создайте в корневой папке и заполните .env файл**:
    
    Пример заполнения находится в папке deploy. 

## Локальный запуск базы данных

1. **Скачайте файл dump.sql**

2. **Создайте базу данных PostgreSQL на вашем компьютере**

3. **Откройте терминал и перейдите в папку со скачанным dump.sql**

   ```bash
    cd C:\Расположение файла
   ```
   
4. **Выполните команду**

   ```bash
    psql -U postgres -d *Название вашей базы данных* < dump.sql
    ```
   
5. **Укажите в .env данные для подключения к вашей БД и сможете запускать проект локально**

## Локальный запуск

1. **Введите в терминал команду**:

    ```bash
    uvicorn api.presentation.api.main:app --reload
    ```

2. **Сайт будет доступен по ссылке**

    http://127.0.0.1:8000/docs
