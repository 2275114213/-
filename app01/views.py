from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth

from  app01.models import  Book, Room
# Create your views here.
def login(request):
        if request.method == 'POST':
            user = request.POST.get('user')
            pwd = request.POST.get('pwd')
            user_obj = auth.authenticate(username=user, password=pwd)
            if user_obj:
                auth.login(request, user_obj)
                # 注册session  request.user 登陆的用户对象
                return  redirect(reverse('index'))

        return render(request,'login.html')

import datetime
def index(request):
    time_choices = Book.time_choices
    room_list = Room.objects.all()
    # 拿预定信息应该以时间为过滤条件
    date = datetime.datetime.now().date()

    # datetime.datetime.now(). 拿到的是年月日, 时分秒 datetime.datetime(2019, 3, 3, 18, 23, 54, 902189)
    # datetime.datetime.now().date()   datetime.date(2019, 3, 3)
    book_date = request.GET.get('book_date',date)  # 如果拿不到就过滤今天的
    book_list = Book.objects.filter(date=book_date)
    htmls = ""
    for room in room_list:
        # 每个room,四列
        htmls += "<tr><td>{}({})</td>".format(room.caption, room.num)
        # 每个时间 td
        for time_choice in time_choices:
            flag = False
            for book in book_list:
                # 在一个时间段一个会议室 只能有一个人预定了, 所以推出循环, 看当前房间的下一个时间段,
                if  book.time_id == time_choice[0] and book.room_id == room.id:

                    flag = True
                    break
            # for  循环不存在作用域, 推出循环的正好是当前匹配成功的信息 极好
            if flag:
                if request.user == book.user:
                    htmls += "<td  class='active item' room_id={} time_id={} class='act'>{}</td>".format(room.id, time_choice[0],
                                                                                book.user)
                else:
                    htmls += "<td  class='other_active item' room_id={} time_id={} class='act'>{}</td>".format(room.id,
                                                                                                    time_choice[0],
                                                                                                    book.user)
            else:
                htmls += "<td room_id={} time_id={} class='item'></td>".format(room.id, time_choice[0])

        htmls += "</tr>"
    # print(html)


    return render(request,"index.html",locals())


def book(request):
        import json
        if request.method == "POST":
            post_data = request.POST.get('post_data')
            post_data = json.loads(post_data)
            chioce_date = request.POST.get("choose_date")
            book_obj_list = []
            print(post_data['ADD'].items())
            for room_id, time_list in post_data['ADD'].items():

                for time_id in time_list:
                    obj = Book(room_id=room_id, time_id=time_id, user_id=request.user.pk, date=chioce_date)
                    book_obj_list.append(obj)
            # 批量创建  批量插入的是 book_obj
            Book.objects.bulk_create(book_obj_list)


            # 删除会议室是预定信息
            for room_id, time_list in post_data['DEL'].items():
                for time_id in time_list:
                    # 这个将进行数据库的多次查询
                    Book.objects.filter(room_id=room_id,time_id=time_id, date=chioce_date, user_id=request.user.pk).delete()
            '''
            yuan先生版本
        for room_id, time_id_list in post_data['DEL'].items():
            for time_id in time_id_list:
                temp = Q()
                temp.connector = 'AND'
                temp.children.append(('user_id', request.user.pk,))
                temp.children.append(('date', choice_date))
                temp.children.append(('room_id', room_id,))
                temp.children.append(('time_id', time_id,))  temp 里面的过滤条件是and , remove_booking
                的 过滤条件是or
                remove_booking.add(temp, 'OR')  
        #         remove_booking ('or', temp,temp1)
        if remove_booking:
            Book.objects.filter(remove_booking).delete()
            
            
            '''



            status_code = {'status':1}

            return HttpResponse(json.dumps(status_code))