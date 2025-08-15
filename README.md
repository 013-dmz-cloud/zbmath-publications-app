# zbmath-publications-app
Приложение за проследяване на научни публикации
# Приложение за проследяване на научни публикации

Това приложение автоматично извлича и анализира публикации на автори от zbMATH.

## Настройка

1. Регистрирайте се за API ключ на [zbMATH API](https://zbmath.org/api/)
2. Създайте `.env` файл в основната директория:
   ```env
   ZBMATH_API_KEY="вашият_api_ключ"
   ```
3. Инсталирайте зависимостите:
   ```bash
   pip install -r requirements.txt
   ```

## Употреба

1. Добавете авторите във `authors.csv`:
   ```csv
   full_name,zbmath_id
   Maya Stoyanova,stoyanova.maya
   ```
2. Стартирайте приложението:
   ```bash
   python main.py
   ```
3. Резултатите ще се съхранят в:
   - Пълен списък: `publications_YYYYMMDD.csv`
   - Нови публикации: `new_publications.csv`

## Примерни данни
- [Примерен authors.csv](authors.csv)
- [Примерен old_publications.csv](old_publications.csv)
