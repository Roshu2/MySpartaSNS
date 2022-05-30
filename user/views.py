from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')

        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '') #None은 유저네임이없다면 빈칸으로 처리하겠다.
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:

            return render(request, 'user/signup.html', {'error': '비밀번호를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 입니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다'}) #사용자가 존재하기 때문에 저장x 회원가입페이지 다시띄움
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio) #밑의 주석코드를 한줄로 줄임

                return redirect('/sign-in')




def sign_in_view(request): #sign_in_view 함수 (요청받은 정보 request)
    if request.method == 'POST': #메소드는 POST다.
        username = request.POST.get('username', '') #유저네임 입력받는다.
        password = request.POST.get('password', '') #비밀번호 입력받는다.

        me = auth.authenticate(request, username=username, password=password) #인증모듈 authenticate

        if me is not None: #위의 코드에서 사용자 정보를 다비교하고 오기때문에 me만 사용한다. me가 비어있지않다면
            auth.login(request, me) #내정보를 넣어준다.로그인 작업을 해준다.
            return redirect('/')  #기본 url로 redirect
        else:
            return render(request, 'user/signin.html', {'error': '유저이름 혹은 비밀번호를 확인 해 주세요'})

    elif request.method == 'GET': #메소드 GET
        user = request.user.is_authenticated
        if user:
            return redirect('/')

        return render(request, 'user/signin.html') #로그인페이지를 띄워준다.


@login_required   #사용자가 로그인이 꼭 되어있어야만 접근이 가능한 함수다.
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')