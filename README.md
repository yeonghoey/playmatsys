# playmatsys

**Nexon Developer Conference 15** "매칭 시스템 구현하기" 세션에서<br>
TrueSkill의 경기 예측과 레이팅 업데이트를 시각적으로 설명하기 위해 구현하였습니다.

## 실행 환경
[kivy][] 프레임워크를 기반으로 구현되었으며 [scipy][]와 [trueskill][] 의존성이 있습니다.

*kivy*는 자체 내장 파이썬을 사용하기 때문에 *scipy*와 *trueskill*을 *kivy* 내장 파이썬 하위에 설치해야합니다.<br>
다음과 같은 과정을 통해 개발환경을 셋팅할 수 있습니다.

    hoey: /Applications/Kivy.app/Contents/Resources/venv/bin $ export PATH=.:$PATH
    hoey: /Applications/Kivy.app/Contents/Resources/venv/bin $ which pip
    ./pip
    hoey: /Applications/Kivy.app/Contents/Resources/venv/bin $ pip install scipy
    hoey: /Applications/Kivy.app/Contents/Resources/venv/bin $ pip install trueskill


[Kivy-1.9.0-ref3-osx.dmg][kivy_install] 버전으로 구현, 테스트되었습니다.

## Screenshot
![screenshot](/screenshot.png)


[kivy_install]: http://kivy.org/#download
[kivy]: http://kivy.org
[scipy]: http://scipy.org
[trueskill]: http://trueskill.org
