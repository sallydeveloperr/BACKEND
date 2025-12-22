from fastapi import FastAPI

# FastAPI 앱
app = FastAPI(
    title='FAST API',
    description="기본기능확인",
    version='0.01'
)

@app.get('/')
def index():
    '''브라우져에서 http://localhost:8000 접속시 실행'''
    return {'message' : '첫번째 화면'}

# 데코레이터 @app.get('/hello') -- 라우터 http://localhost:8000/hello --> 서버 내의 해당 함수를 실행
# @app.get('/hello')
@app.get('/hello')
def say_hello():
    return {'message' : 'Hello World'}

# 경로 파라메터 vs 쿼리 파라메터
# http://localhost:8000/hello/홍길동 - 경로 파라메터
@app.get('/hello/{name}')
def say_hello(name:str):
    return {'message' : f'Hello {name}'}       # 자동으로 json 형태로 변환

@app.get('/greet')  # http://localhost:8000/greet?name=홍길동&age=35
def greet(name:str, age:int):
    return f"반갑습니다. {name}님 당신은 나이는 {age}입니다."

@app.get('/multiply')
def multiply(num1: int, num2: int):
    return num1 * num2

# /multiply 엔드포인트를 만들어서 두 숫자를 입력받아서 곱해서 출력하기
# /hello/{name}에 쿼리 파라메터로 lang을 추가해서 
    # lang=ko -> 안녕하세요
    # lang=en -> hello 
@app.get('/hellolang')
def say_hello_ko(name:str, lang:str):
    '''두 개의 파라메터를 쿼리 스트링으로 전달'''
    if lang == 'ko':
        return {'message' : f'안녕하세요 {name} 님'}    #http://localhost:8000/hellolang?name=홍길동&lang=ko
    elif lang == 'en':
        return {'message' : f'Hello {name} sir'}    #http://localhost:8000/hellolang?name=홍길동&lang=en
    else:
        return f"lang 정보를 입력하세요 ?name=이름&lang=언어"