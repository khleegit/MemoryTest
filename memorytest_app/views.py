from django.shortcuts import render
from django.http import HttpResponse
import random
import os

# 단어 리스트 파일 경로
WORDS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'nouns.txt')

def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

words_list = load_words(WORDS_FILE_PATH)

def index(request):
    if 'level' not in request.session:
        request.session['level'] = 3  # 처음에는 3개의 단어를 표시

    level = request.session['level']
    words = random.sample(words_list, level)
    context = {
        'words': words
    }
    return render(request, 'index.html', context)

def check(request):
    if request.method == 'POST':
        given_words = request.POST.getlist('words')
        correct_words = request.POST.getlist('correct_words')
        correct_count = sum(1 for given_word, correct_word in zip(given_words, correct_words) if given_word == correct_word)
        total = len(correct_words)

        if correct_count == total:
            request.session['level'] += 1  # 맞춘 경우 단어 개수 1개 증가
            message = f"정답입니다! {total}개의 단어를 모두 맞췄습니다."
        else:
            request.session['level'] = 3  # 틀린 경우 다시 3개로 초기화
            message = f"틀렸습니다. {total}개의 단어 중 {correct_count}개를 맞췄습니다."

        context = {
            'message': message,
            'given_words': given_words,
            'correct_words': correct_words
        }
        return render(request, 'result.html', context)
    return HttpResponse("Invalid request")
