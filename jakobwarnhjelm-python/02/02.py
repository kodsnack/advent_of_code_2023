# with open("example.txt") as file:
maxvalues = {
    "red" : 12,
    "blue" : 14,
    "green" :13
}
idsum = 0
# with open("example.txt") as file:    
with open("input.txt") as file:        
    while line := file.readline():
        game = line.split(':')[0]
        gameNumber = game[5:]
        print(gameNumber)

        maxValueExceededCount =  0

        draws = line.split(':')[1].split(';')
        # print(draws)
        for draw in draws:
            # print(draw)
            blocks = draw.split(',')
            # print(blocks)
            for block in blocks:
                # print(block)
                blocksplit =block.split(" ")
                # print(blocksplit)
                # print(point)
                
                point = int(blocksplit[1])
                color = blocksplit[2].rstrip()
                # print(color)
                print(str(point) + " " + color)
                if point > maxvalues[color]:
                    print("maxvals exceeded")
                    maxValueExceededCount +=1
        if maxValueExceededCount == 0:
            idsum += int(gameNumber)

print(idsum)
        
