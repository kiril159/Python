a_name = list(input())
z_name = list(input())
f_name = []
for i in range(len(z_name)):
    if z_name[i] in a_name:
        if z_name[i] == a_name[i]:
            f_name.append('P')
            a_name[i] = 0
        else:
            p = a_name.index(z_name[i])
            if not a_name[p] == z_name[p]:
                a_name[p] = 0
                f_name.append('S')
            else:
                f_name.append('I')
    else:
        f_name.append('I')
print(''.join(f_name))


'''a_name = list(input())
z_name = list(input())
f_name = [0 for i in range(len(a_name))]
for i in range(len(a_name)):
    if z_name[i] == a_name[i]:
        f_name[i] = 'P'
        a_name[i] = 0
for i in range(len(a_name)):
    if not f_name[i] == 'P':
        if z_name[i] in a_name:
            if not a_name[a_name.index(z_name[i])] == z_name[a_name.index(z_name[i])]:
                a_name[a_name.index(z_name[i])] = 0
                f_name[i] = 'S'
            else:
                f_name[i] = 'I'
        else:
            f_name[i] = 'I'
print(''.join(f_name))'''