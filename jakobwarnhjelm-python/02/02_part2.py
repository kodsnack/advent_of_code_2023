idsum = 0
# with open("example.txt") as file:    
with open("input.txt") as file:        
    while line := file.readline():
        lowvalues = {
            "red" : 0,
            "blue" : 0,
            "green" :0
        }        
        game = line.split(':')[0]
        gameNumber = game[5:]
        print(gameNumber)

        maxValueExceededCount =  0

        draws = line.split(':')[1].split(';')
        for draw in draws:
            blocks = draw.split(',')
            for block in blocks:
                blocksplit =block.split(" ")
                point = int(blocksplit[1])
                color = blocksplit[2].rstrip()
                if point > lowvalues[color]:
                    lowvalues[color]=point

        # print(lowvalues)
        gamepower = lowvalues['red']*lowvalues['green']*lowvalues['blue']
        # print(gamepower)
        idsum += gamepower
print(idsum)
        
