import gkit
import time

TRY_LIMIT = 3
PASSWORD = '기가지니'


def main():
    gkit.tts_play('암호를 입력 하시겠습니까')
    text = gkit.getVoice2Text()
    print(text)
    # yes
    if (text.find('예') >= 0):
        gkit.tts_play('환영')
        for no_try in range(TRY_LIMIT):
            password = gkit.getVoice2Text()
            print(password)
            if (password.find(PASSWORD) >= 0 and len(password) <= 3 * len(PASSWORD)):
                # welcome
                gkit.tts_play('환영')
                print('WELCOME')
                break
            elif no_try < TRY_LIMIT - 1:
                # please try again
                gkit.tts_play('다시 시도해주세요.')
    else:
        # see you again
        gkit.tts_play('또 보자')


if __name__ == '__main__':
    main()
