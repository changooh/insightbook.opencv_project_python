# 예외 이름을 모르는 경우 처리 방법
# 모든 에러 처리
# 에러 이름 확인
try:
    List = []
    print(List[0])  # 에러가 발생할 가능성이 있는 코드

except Exception as ex:  # 에러 종류
    print('에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수


# 에러를 직접 일으키는 방법 - raise # 사용자가 직접 에러를 발생시키는 기능
# 단점, 많이 사용하면 코드를 읽기 어려워진다.

# 올바른 값을 넣지 않으면 에러를 발생시키고 적당한 문구를 표시한다.
def rsp(mine, yours):
    allowed = ['가위', '바위', '보']
    if mine not in allowed:
        raise ValueError
    if yours not in allowed:
        raise ValueError


try:
    rsp('가위', '바')
except ValueError:
    print('잘못된 값을 넣었습니다!')
# 190이 넘는 학생을 발견하면 반복을 종료한다.
school = {'1반': [150, 156, 179, 191, 199], '2반': [150, 195, 179, 191, 199]}

try:
    for class_number, students in school.items():
        for student in students:
            if student > 190:
                print(class_number, '190을 넘는 학생이 있습니다.')
                # break # 바로 상위 for문은 종료되지만 최고 상위 for문은 종료되지 않는다.
                raise StopIteration
                # 예외가 try 문 안에 있지 않으면 에러 발생시 프로그램이 멈춘다.
except StopIteration:
    print('정상종료')
