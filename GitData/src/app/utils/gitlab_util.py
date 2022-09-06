# TODO Убрать захардкоженный токен.
#  Возможно, сделать функционал для использования персональных токенов каждым пользователем

import gitlab

group = 'MyNameIsKirill'
group_id = 56097138

branch = 'main'

user_token = "glpat-uNdTxsJnZsnuYvbL9cLr"



gl = gitlab.Gitlab(private_token=user_token) #url='https://git.finch.fm',
gl.auth()

