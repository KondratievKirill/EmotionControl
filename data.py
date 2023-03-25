def new_user(user):
    users = open('users.txt', 'r+')
    li_us = users.read()
    if li_us == '':
        users.write(user)
    else:   
        li_us = li_us.split('/')
        if user in li_us:
            users.close()
        else:
            users.write('/' + user  )
            users.close()
def user_list():
    users = open('users.txt', 'r+')
    li_us = users.read()
    li_us = li_us.split('/')
    return li_us
    users.close()