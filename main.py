import os
import csv
import requests
import time
from datetime import datetime
import pandas as pd

# Конфигурация
API_KEY = os.getenv('ZBMATH_API_KEY')  # Environment variable за сигурност
AUTHORS_FILE = "authors.csv"
OLD_PUB_FILE = "old_publications.csv"
NEW_PUB_FILE = "new_publications.csv"
FULL_PUB_FILE = f"publications_{datetime.now().strftime('%Y%m%d')}.csv"

def get_author_publications(author_id):
    """Извлича публикациите за даден автор от zbMATH API"""
    url = f"https://zbmath.org/api/v1/authors/{author_id}/publications/?apikey={API_KEY}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('publications', [])
    except requests.exceptions.RequestException as e:
        print(f"Грешка при извличане на публикации за {author_id}: {str(e)}")
        return []

def process_publication(pub):
    """Обработва данните за публикацията"""
    return {
        'zbl_id': pub.get('zbl_id', ''),
        'title': pub.get('title', {}).get('text', ''),
        'year': pub.get('year', ''),
        'authors': '; '.join(a['display_name'] for a in pub.get('authors', [])),
        'source': pub.get('journal', {}).get('name', ''),
        'link': f"https://zbmath.org/{pub.get('zbl_id', '')}"
    }

def fetch_all_publications():
    """Извлича всички публикации за авторите"""
    all_publications = []
    
    with open(AUTHORS_FILE, 'r') as f:
        authors = list(csv.DictReader(f))
    
    print(f"\nОбработване на {len(authors)} автора...")
    
    for idx, author in enumerate(authors, 1):
        print(f"{idx}/{len(authors)}: Извличане на {author['full_name']} ({author['zbmath_id']})")
        pubs = get_author_publications(author['zbmath_id'])
        
        for pub in pubs:
            pub_data = process_publication(pub)
            pub_data['author_id'] = author['zbmath_id']
            all_publications.append(pub_data)
        
        time.sleep(1.5)  # Спазване на rate limits
    
    # Запис на пълния CSV
    if all_publications:
        with open(FULL_PUB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_publications[0].keys())
            writer.writeheader()
            writer.writerows(all_publications)
    
    print(f"\n✅ Записани {len(all_publications)} публикации във {FULL_PUB_FILE}")
    return all_publications

def find_new_publications(all_pubs):
    """Намира новите публикации спрямо стария файл"""
    if not os.path.exists(OLD_PUB_FILE):
        print("\n⚠️ Няма стар файл за сравнение. Всички публикации ще се считат за нови.")
        new_publications = all_pubs
    else:
        # Зареждане на старите публикации
        old_pubs = pd.read_csv(OLD_PUB_FILE)
        old_zbl_ids = set(old_pubs['zbl_id']) if not old_pubs.empty else set()
        
        # Филтриране на новите
        new_publications = [pub for pub in all_pubs if pub['zbl_id'] not in old_zbl_ids]
    
    # Запис на новите
    if new_publications:
        with open(NEW_PUB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=new_publications[0].keys())
            writer.writeheader()
            writer.writerows(new_publications)
    
    print(f"\n🔍 Намерени {len(new_publications)} нови публикации")
    return new_publications

def main():
    print("="*50)
    print(" Приложение за проследяване на научни публикации")
    print(" В базата данни на zbMATH")
    print("="*50)
    
    # Създаване на примерни файлове ако липсват
    if not os.path.exists(AUTHORS_FILE):
        with open(AUTHORS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['full_name', 'zbmath_id'])
            writer.writeheader()
            writer.writerow({'full_name': 'Maya Stoyanova', 'zbmath_id': 'stoyanova.maya'})
            writer.writerow({'full_name': 'Ivan Ivanov', 'zbmath_id': 'ivanov.ivan'})
        print(f"\n✅ Създаден примерен {AUTHORS_FILE}")
    
    if not os.path.exists(OLD_PUB_FILE):
        open(OLD_PUB_FILE, 'a').close()  # Създаване на празен файл
        print(f"✅ Създаден празен {OLD_PUB_FILE} за сравнение")
    
    # Основна логика
    all_pubs = fetch_all_publications()
    new_pubs = find_new_publications(all_pubs)
    
    # Краен изход
    print("\n" + "="*50)
    print(" Действията завършиха успешно!")
    if new_pubs:
        print(f"🌟 Открити са {len(new_pubs)} НОВИ публикации във {NEW_PUB_FILE}")
    else:
        print("ℹ️ Няма нови публикации")
    print("="*50)

if __name__ == "__main__":
    main()
