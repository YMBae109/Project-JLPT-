import pygame
import random
import color
import csv
import tkinter as tk
from tkinter import simpledialog

pygame.init()

# 화면크기
screen_width = 1280
screen_height = 853
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("JLPT Game")

# 폰트 설정 (시스템 폰트 사용)
font_jpn = pygame.font.SysFont('Meiryo', 48)  # 일본어를 위한 메이리오 폰트
font_kor = pygame.font.SysFont('Malgun Gothic', 36)  # 한글을 위한 맑은 고딕 폰트
font_hiragana = pygame.font.SysFont('Meiryo', 10)
# 배경 이미지 로드
# background_image = pygame.image.load('Image\\바다2.jpg')

# CSV 파일에서 단어 읽기
def load_words_from_csv(filename):
    words = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            words.append(row)
    return words

# N2, N3 단어 목록 불러오기
n2_words = load_words_from_csv('n2_words.csv')
n3_words = load_words_from_csv('n3_words.csv')

# 난이도 선택 화면
def choose_level():
    selecting = True
    level = None
    while selecting:
        # screen.blit(background_image, (0, 0))
        screen.fill(color.white)
        level_text = font_kor.render("난이도를 선택하세요", True, (color.black))
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, screen_height // 3))

        n2_text = font_kor.render("1: N2 단어", True, (color.red))
        n3_text = font_kor.render("2: N3 단어", True, (color.blue))
        screen.blit(n2_text, (screen_width // 2 - n2_text.get_width() // 2, screen_height // 2))
        screen.blit(n3_text, (screen_width // 2 - n3_text.get_width() // 2, screen_height // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = n2_words
                    selecting = False
                elif event.key == pygame.K_2:
                    level = n3_words
                    selecting = False

    return level

# 난이도와 게임 모드 선택
current_words = choose_level()

# 사용자 정의 이벤트 생성
SPAWN_SQUARE = pygame.USEREVENT + 1

# 타이머 설정: 2초마다 SPAWN_ENEMY 이벤트가 발생
pygame.time.set_timer(SPAWN_SQUARE, 4000)

# 시간 객체 생성
clock = pygame.time.Clock()

# 단어 상자 리스트
falling_word = []
# 오답 단어상자 리스트
fallied_word = []
# 사용자 입력 저장 변수
user_input = ''

# 단어 생성 함수
def fall_word():
    word_data = random.choice(current_words)
    x_position = random.randint(0, screen_width - 200)
    word_color = random.choice([color.red, color.blue])
    word_surface = font_jpn.render(word_data["kanji"], True, word_color) # 한자를 화면에 표시
    word_rect = word_surface.get_rect(topleft=(x_position, 0))
    falling_word.append((word_surface, word_rect, word_data))

# 이동 속도 설정
speed = 20

# 게임 루프
running = True

# 입력 도형 
input_box = pygame.Rect(screen_width // 2 - 200, screen_height - 100, 400, 50)

# 실패한 단어를 공부하는 함수
def review_failed_words():
    reviewing = True
    while reviewing:
        screen.fill(color.white)
        # screen.blit(background_image, (0, 0))
        review_text = font_kor.render("못 푼 단어를 다시 공부하세요!", True, color.black)
        screen.blit(review_text, (screen_width // 2 - review_text.get_width() // 2, 50))

        for index, word in enumerate(fallied_word):
            word_surface = font_jpn.render(word[2]["kanji"], True, color.red)
            hiragana = font_hiragana.render(word[2]["hiragana"], True, color.black)
            meaning_surface = font_kor.render(word[2]["meaning"], True, color.blue)
            screen.blit(word_surface, (100, 150 + index * 60))
            screen.blit(hiragana, (110, 145 + index * 60))
            screen.blit(meaning_surface, (400, 150 + index * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reviewing = False
                pygame.quit()
                quit()
                
# Tkinter를 통한 한글 입력 처리
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("입력", "정답을 입력하세요:")

while running:
    # 델타 타임 계산
    dt = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_SQUARE:
            fall_word()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                user_input = get_user_input()
                if user_input:
                    for word_surface, word_rect, word_data in falling_word[:]:
                        if user_input == word_data["meaning"]:
                            falling_word.remove((word_surface, word_rect, word_data))
                    user_input = ''
            if event.key == pygame.K_ESCAPE:
                review_failed_words()
                break
    # 단어 이동
    for word in falling_word[:]:
        word[1].y += speed * dt
        if word[1].top > screen_height:
            fallied_word.append(word)
            falling_word.remove(word)

    screen.fill(color.white)
    
    # 배경 이미지 그리기
    # screen.blit(background_image, (0, 0))
    # 단어 상자 그리기
    for word_surface, word_rect, word_data in falling_word:
        screen.blit(word_surface, word_rect)
    
    # 사용자 입력 표시
    input_surface = font_kor.render(user_input, True, color.black)
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

    pygame.display.flip()
 
pygame.quit()