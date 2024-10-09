# DuckChain Telegram Bot
Скрипт для автоматического выполнения заданий в DuckChain

[TELEGRAM CHANNEL](https://t.me/cucumber_scripts)

## Обновления
- **09.10.24** Задания выполняются для всех категорий, а не только для Partner


# Регистрация
DuckChain работает на сети TON L2, поддерживаемой Arbitrum, и стремится привлечь ликвидность и пользователей из 
экосистем Ethereum Virtual Machine (EVM) и Bitcoin в экосистему TON.

Для регистрации в боте перейдите по ссылке : [https://t.me/DuckChain_bot/](https://t.me/DuckChain_bot/quack?startapp=hUOAQXRd)


## Функции
- Ежедневная проверка: Автоматизация ежедневных входов.
- Открытие ящиков: Автоматическое открытие всех доступных ящиков.
- Завершение задач: Автоматическое завершение доступных задач.
- Поддержка прокси: Возможность использования прокси для управления несколькими аккаунтами.
- Конфигурация: Легкая настройка через файл config.json.

### Example Log Output
   ```yaml
Processing account 1 / 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[2024-09-15 13:22:57] Duck name: Quacky123
[2024-09-15 13:22:57] Decibels: 45 | Box Amount: 1
[2024-09-15 13:22:57] Daily Check-in successfully
[2024-09-15 13:22:57] Box opened successfully!
[2024-09-15 13:22:57] Quantity: 1 | Points: 100 | Boxes left: 2
[2024-09-15 13:22:57] All boxes opened! No more boxes left.
[2024-09-15 13:22:57] Quack 1: SUCCESS | Result: Some random result
[2024-09-15 13:22:57] Decibel Change: 10 | Quack Times: 1
[2024-09-15 13:22:57] Task successfully completed! Reward 5 Points
   ```


## Инструкции по установке

1. **Клонируйте репозиторий**

   ```bash
   git clone https://github.com/cucumber-pickle/DuckChainCucu.git
   cd DuckChainCucu
   ```

2. **Создайте виртуальную среду (не обязательно):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

   
3. **Установите зависимости::**


  ```bash
    pip install -r requirements.txt
  ```



## Настройки:


   ```json

{
   "use_proxy": false,
   "quack_delay": 2,
   "quack_amount": 5,
   "complete_task": false,
   "account_delay": 5,
   "countdown_loop": 3600
}
   ```
- `use_proxy`: Включить или отключить использование прокси (true/false).
- `quack_delay`: Время (в секундах) между кваками.
- `quack_amount`: Количество кваков на аккаунт.
- `complete_task`: Включить или отключить автоматическое завершение задач (true/false).
- `account_delay`: Задержка (в секундах) между обработкой каждого аккаунта.
- `countdown_loop`: Время (в секундах) перед перезапуском цикла бота.

## Настройка запросов:

Добавьте токены вашего аккаунта DuckChain в файл с именем data.txt в корневом каталоге, каждый токен на новой строке.

Example:
   ```txt
Query_id1
Query_id2
Query_id3
   ```
### Настройка прокси:

Если вы используете прокси, создайте файл proxies.txt в корневом каталоге с одним прокси на строку в формате:

Example (proxy format: username:password@host:port):

   ```graphql
user1:pass1@123.123.123.123:8080
user2:pass2@456.456.456.456:8080
   ```

## Использование
Запустите скрипт с помощью:

   ```bash
python main.py
   ```

***Функциональность бота:***

Бот загрузит аккаунты из data.txt, обработает каждый аккаунт, получив информацию о пользователе, 
выполнит ежедневный вход, откроет все ящики, выполнит кваки и завершит задачи, если это включено.

## Где взять tgWebAppData (query_id / user_id)

1. Запустите телеграм portable или вэб версию
2. Запустите приложение, для которого хотите получить дату
3. Нажмите `F12` на клавиатуре (или правой кнопкой мыши и "проверить" в ТГ portable)
4. Откройте вкладку консоль
5. Вставьте этот код в консоль:

```javascript
copy(Telegram.WebApp.initData)
```

6. Вы получите tgWebAppData, которая выглядит вот так:

```
query_id=AA....
user=%7B%22id%....
```
7. Добавьте ее в файл `data.txt` 


## Этот бот был Вам полезен? Пожалуйста, подписывайтесь на канал или можете купить мне кофе: 
``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - BSC (BEP 20)

``` UQBiNbT2cqf5gLwjvfstTYvsScNj-nJZlN2NSmZ97rTcvKz0 ``` - TON

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - Optimism

``` THaLf1cdEoaA73Kk5yiKmcRwUTuouXjM17 ``` - TRX (TRC 20)

## License
This project is licensed under the `MIT License`.

## Контакты
Для дальнейших вопросов или поддержки свяжитесь через Telegram по адресу [CUCUMBER TG CHAT](https://t.me/cucumber_scripts_chat)