import requests
from datetime import datetime


def get_questions(days_ago, tag):
    counter = 0
    todate = int(datetime.timestamp(datetime.today()))
    fromdate = todate - days_ago * 86400
    question_create_time, counter = get_next_questions(fromdate, todate, tag, counter)
    while question_create_time < todate:
        question_create_time, counter = get_next_questions(question_create_time, todate, tag, counter)
        question_create_time += 1
    return f'За {days_ago} дня(-ей) опубликовано {counter} новых вопросов.'


def get_next_questions(fromdate, todate, tag, counter):
    question_create_time = todate
    params = {
        'fromdate': fromdate,
        'todate': todate,
        'order': 'asc',
        'sort': 'creation',
        'tagged': tag,
        'site': 'stackoverflow'
    }
    
    responce = requests.get('https://api.stackexchange.com/2.3/questions', params=params)
    responce.raise_for_status()
    if responce.status_code != 200:
        print(f"Ошибка обработки запроса! Код ошибки: {responce.status_code}")
        return question_create_time, counter
    for question in responce.json().get('items'):
        counter += 1
        question_create_time = question['creation_date']
        with open(f'last_questions_{datetime.fromtimestamp(todate)}.txt', 'a') as file:
            file.write(f'Question # {counter}: {question["title"]}\n'
                       f'Tags: {str(question["tags"])}\n '
                       f'Creation Date {datetime.fromtimestamp(question_create_time)}\n'
                       f'___\n')
        print(f'Question # {counter}: {question["title"]}')
        print(f'Tags: {str(question["tags"])}')
        print(f'Creation Time: {datetime.fromtimestamp(question_create_time)}')
        print('___')

    return question_create_time, counter


if __name__ == '__main__':
    print(get_questions(2, 'python'))