# with open("example.txt") as file:
with open("input.txt") as file:    
    calsum = 0
    while line := file.readline():
        # str = line.lower().strip('abcdefghijklmnopqrstuvwxyzåäö')
        s=''.join(i for i in line if i.isdigit())
        # print(str.rstrip())
        # print(s)
        nbr = int(s[0] + s[len(s)-1])
        # last = int()
        # print(nbr)
        calsum += nbr
    print(calsum)
