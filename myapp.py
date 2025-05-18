import requests
import os
import pprint
import random
import html


def main():
    while True:
        try:
            categories = get_categories()
            print_categories(categories)
            selected_category_id = get_input('Select a category', len(categories))
            selected_category = [category for category in categories if selected_category_id + 8 == category['id']][0]
            os.system('clear')
            print(f'You selected the following category: {selected_category["name"]}')        
            questions = [q for q in get_questions(selected_category_id)['results'] if q['type']=='multiple']
            again = play(questions[:3])
            if not again:
                print('\nBye!')
                return
        except Exception as e:
            print('⛔️', e.args[0])
            return False
    
def play(questions):
    score = 0
    for q in questions:
        answers = q['incorrect_answers']+ [q['correct_answer']]
        print_question(q, answers)
        answer_index = get_input('Your answer', len(q['incorrect_answers']) + 1) - 1
        if answers[answer_index] == q['correct_answer']:            
            print('Correct!')
            score += 1
        else:
            print('Wrong! The correct answer is', encode(q['correct_answer']))
            
    print(f'\nYour quiz completed. Your final score is {score}/{len(questions)}\n')
    again = input('Do you want to play another game? y/n: ')
    if again in ['y', 'Y']:
        return True
    return False
    
   
def print_question(question, answers):    
    print()
    print(encode(question['question']))
    random.shuffle(answers)
    for idx, a in enumerate(answers):

        print(f"{idx+1}. {encode(a)}")
        

def encode(text:str) -> str:
    subs = {
        '&#039;': '\'',
        '&quot;': '"',
    }
    result = text
    for sub in subs:      
        result = result.replace(sub, subs[sub])
    return result

    
def get_questions(category_id:int) -> list:
    url = f'https://opentdb.com/api.php?amount=10&category={category_id+8}'
    try:
        data = requests.get(url, timeout=10)
        return data.json()
    except:
        raise Exception('Error fecthing questions ❓, please try again later! ')
    
    
def print_categories(categories):
    for cat in categories:
        print(f"{cat['id']-8:>2d}. {cat['name']}")
    
    
def get_categories():
    url = 'https://opentdb.com/api_category.php'
    print('Fetching categories...')
    try:
        data = requests.get(url, timeout=1)
        categories = data.json()['trivia_categories']
    except Exception as e:        
        raise Exception('Error fecthing categories 📁, please try again later!')
        
    return categories
    

def get_input(text:str, rng: int) -> int:
    choices = "/".join([str(n) for n in range(1, rng+1)])
    while True:
        answer = input(f'{text} ({choices}): ')
        try:
            result = int(answer)
            if not (1 <= result <= rng):
                print('Please select a valid choice!')
                continue
            return result
        except:
            print('Please select a valid choice!')
            continue


if __name__ == '__main__':
    main()
    # t = encode('In The Lies Of Locke Lamora, what does &quot;Lamora&quot; mean in Throne Therin?')
    # print(t)