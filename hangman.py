#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Author: Phillipe Smith <phsmithcc@gmail.com>
# Description: Simple Python Hangman
# Version: 0.1

import os, sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from random import randint
from time import sleep

class Hangman:
    picture = r'''
    +-------+
    |       |
    |       O
    |      /|\
    |      / \
    |
===================
'''
    wordlist_url = 'https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt'

    doll_body_map = [
        71, # Right leg
        69, # Left leg
        56, # Right Arm
        54, # Left Arm
        55, # Body
        41, # Head
    ]


    def __init__(self):
        self.errors  = 0
        self.hits    = 0
        self.wordlist_file = '/tmp/wordlist.txt'

        try:
            self.wordlist = open(self.wordlist_file, 'r').read().split('\n')
        except Exception as e:
            try:
                print('   JOGO DA FORCA\n====================\n')
                print(f'Aguarde....\nBuscando lista de palavras no endereço:\n{self.wordlist_url}.....')
                sleep(2)

                response = urlopen(self.wordlist_url)
                self.wordlist = response.read().decode()

                # Write to file
                with open(self.wordlist_file, 'w') as fh:
                    fh.write(self.wordlist)

                self.wordlist = self.wordlist.split('\n')
            except HTTPError as e:
                sys.exit('\nO servidor não conseguiu atender a solicitação...\n%s\n' % e)
            except URLError as e:
                sys.exit('\nFalha ao contactar o servidor...\n%s\n' % e)

    def kick(self, chars):
        kick = input('Chute uma letra [ 0 = sair ]: ').upper()

        if kick == '0':
            sys.exit('\nObrigado por jogar!\n')

        if kick.isalpha() and len(kick) == 1 and kick not in chars:
            if kick in self.sorted_word:
                self.correct += kick
                for i in range(len(self.sorted_word)):
                    if '-' == self.sorted_word[i]:
                        self.word[i] = '-'
                    if kick == self.sorted_word[i]:
                        self.word[i] = kick
            else:
                print('Não há a letra "%s" na palavra... Tente outra...' % kick)
                sleep(2)
                self.wrong += kick
                return kick

    def result(self):
        if ''.join(self.word) == self.sorted_word:
            self.hits += 1
            print('Você acertou! Parabéns!\n')
            self.play() if self.again() else sys.exit()
        else:
            if self.n_wrong != len(self.doll_body_map):
                self.kick(self.kicks)
            else:
                self.errors += 1
                print('Você Perdeu... A palavra era: %s\n' % self.sorted_word)
                self.play() if self.again() else sys.exit()
        return

    def draw(self):
        self.n_wrong = len(self.wrong)
        self.kicks   = self.correct + self.wrong
        draw_picture = self.picture
        draw_header  = '===================='
        draw_points  = '[ Acertos: %s - Erros: %s ]' % (self.hits, self.errors)

        if self.n_wrong <= len(self.doll_body_map):
            for i in range(self.n_wrong):
                draw_picture = draw_picture[:self.doll_body_map[i]] + ' ' + draw_picture[self.doll_body_map[i]+1:]

            print('   JOGO DA FORCA\t%s\n%s\n%s' % (draw_points, draw_header, draw_picture))
            print('Chutes: %s\nPalavra: %s\n' % (' '.join(self.kicks), ' '.join(self.word)))

            self.result()

    def again(self):
        play_again  = input('Deseja jogar novamente [s ou n]: ').lower()
        self.points = '[ Acertos: %s - Erros: %s ]' % (self.hits, self.errors)

        if play_again and play_again[0].lower() == 's':
            print('Aguarde enquanto o jogo é carregado...\n')
            return True
        else:
            print('\nObrigado por jogar!\n')
            return False

    def play(self):
        self.correct = ''
        self.wrong   = ''
        self.sorted_word = self.wordlist[randint(0, len(self.wordlist))].upper()
        self.word = ['_'] * len(self.sorted_word)

        while len(self.wrong) <= len(self.doll_body_map):
            os.system('cls') if sys.platform.find('win') > -1 else os.system('clear')
            self.draw()


if __name__ == '__main__':
    game = Hangman()
    game.play()
