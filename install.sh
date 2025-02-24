#!/bin/bash

# Установка необходимых зависимостей
echo "Обновление списка пакетов и установка зависимостей..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip mysql-server

# Установка Python-библиотек
echo "Установка зависимостей Python..."
pip3 install -r /usr/local/animal-shelter/requirements.txt

# Создание базы данных и таблиц в MySQL
echo "Настройка базы данных MySQL..."

# Пароль для root пользователя MySQL
DB_ROOT_PASSWORD="root_password"  # Убедитесь, что пароль безопасный и его нужно будет заменить на свой

# Создаем базу данных
mysql -u root -p$DB_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS animal_shelter;"

# Создаем таблицы, если их еще нет
mysql -u root -p$DB_ROOT_PASSWORD animal_shelter < /usr/local/animal-shelter/animal_shelter/sql/schema.sql

echo "База данных и таблицы созданы."

echo "Установка завершена."
