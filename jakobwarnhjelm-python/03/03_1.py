savedCoords=[]

def concat_coords(nbrA, nbrB):
    return str(nbrA)+"," + str(nbrB)

def save_coord(nbrA, nbrB):
    print("Saving coords " + concat_coords(nbrA, nbrB))
    savedCoords.append(concat_coords(nbrA, nbrB))

def coordsExistsInList(nbrA, nbrB):
    if concat_coords(nbrA, nbrB) in savedCoords:
        return True
    else:
        return False

# with open("example.txt") as file:    
with open("input.txt") as file: 
    summer = 0
    txtList = []
    while line := file.readline():
        # rowList = line.split()
        # print(rowList)
        line = line.rstrip()
        txtList.append([*line])
    # print(txtList[9][2])

    combolist = [-1, 0, 1]
    noOfCols = len(txtList[0])
    noOfRows = len(txtList)
    print("noOfCols " + str(noOfCols))
    print("noOfRows " + str(noOfRows))

    for i in range(noOfRows):
        for j in range(noOfCols):
            # print(txtList[i][j])
            adjacentString = ""

            elm = txtList[i][j]



            if elm.isdigit():
                for k_elm in combolist:
                    for l_elm in combolist:
                        rowcoord = i + k_elm
                        colcoord = j + l_elm
                        prtstring = ""
                        prtstring = "(" + str(k_elm) + ", " + str(l_elm) + ")" + "(" + str(rowcoord) + ", " + str(colcoord) + ")"
                        if rowcoord>=0 and rowcoord<noOfRows and colcoord>=0 and colcoord<noOfCols and not (k_elm==0 and l_elm==0):
                            adjacentString += txtList[rowcoord][colcoord]
                            # prtstring += txtList[rowcoord][colcoord]
                            # prtstring += "(" + str(k_elm) + ", " + str(l_elm) + ")"
                            prtstring += " VALID " + txtList[rowcoord][colcoord]
                        # print(prtstring)
                        # break
            # print("(" + str(i) + ","+ str(j) + ") =" + str(elm) + " : " + adjacentString + "    " + prtstring)


                strp = adjacentString.replace('.', '')
                strp = ''.join([i for i in strp if not i.isdigit()])


                if len(strp)>0 and coordsExistsInList(i, j)==False:
                    # print(elm + " " + adjacentString + " ::: " + strp)
                    # print("har symboler adjacent")
                    save_coord(i, j)

                    #konstruera siffra
                    nbrStr = elm
                    lastElm = elm

                    # gå vänster
                    jj = j
                    lastElmIsNumber = True

                    while lastElmIsNumber:
                        jj = jj-1
                        if jj>=0:
                            lastElm = txtList[i][jj]
                            # print(lastElm)
                        else:
                            break
                        if lastElm.isdigit() and coordsExistsInList(i, jj)==False:
                            nbrStr = lastElm + nbrStr
                            lastElmIsNumber = True
                            save_coord(i, jj)
                        else:
                            lastElmIsNumber = False

                    # gå höger
                    jj = j
                    lastElmIsNumber = True
                    while lastElmIsNumber:
                        jj = jj+1
                        if jj<noOfCols:
                            lastElm = txtList[i][jj]
                        else:
                            break
                        if lastElm.isdigit() and coordsExistsInList(i, jj)==False:
                            nbrStr = nbrStr + lastElm
                            lastElmIsNumber = True
                            save_coord(i, jj)
                        else:
                            lastElmIsNumber = False

                    print("NUMBER " + nbrStr)       
                    summer += int(nbrStr)    




            # uppe vänster -1,-1
            # vänster 0, -1
            # nere vänster 1,-1
            # nere 1, 0
            # nere höger 1, 1
            # höger 0, 1
            # uppe höger -1, 1
            # uppe -1, 0
    print(summer)

