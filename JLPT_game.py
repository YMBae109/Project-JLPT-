import pygame
import random
import color
import csv

pygame.init()

# 화면크기
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 폰트 설정
font = pygame.font.Font(None, 36)

## <<-- fps 적용을 위한 시간 객체 생성
clock = pygame.time.Clock()

## 환경 변수

# csv 파일에서 데이터 불러오기
def load_words_from_csv(filename):
    words = []
    with open(filename, mode='r', encoding='utf_8') as file:
        reader = csv.reader(file)
        next(reader)  # 첫 번째 행(헤더)을 건너뜁니다
        for row in reader:
            words.append({'kanji': row[0], 'hiragana': row[1], 'meaning': row[2], 'level': row[3]})
    return words

# N2 단어 목록 불러오기
n2_words = load_words_from_csv('n2_words.csv')

# N3 단어 목록 불러오기
n3_words = load_words_from_csv('n3_words.csv')

## <<--- 메인 루프
running = True


# 2. Event Handling & Image creation
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))
    
# 3. Termination
pygame.quit()