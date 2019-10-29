a = ['a','b$','c$','aaa','-$','0.33','haha']
b = []
temp = ''
for i in a:
    if i[-1] != '$':
        b.append(temp + i)
        temp = ''
        print(b)
    else:
        temp = temp + i.rstrip('$')
        print(b)



print("finally:")
print(b)
