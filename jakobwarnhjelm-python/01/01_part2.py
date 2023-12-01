txt = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
txt_nbr = [1,2,3,4,5,6,7,8,9]

linecounter = 0
calsum = 0
# with open("example2.txt") as file:
with open("input.txt") as file:
    while line := file.readline():
        linecounter += 1

        #sök från vänster
        idx_left_str = len(line)
        left_nbr_str = ""
        for idx, nb in enumerate(txt):
            tmp_idx = line.find(nb)
            # print(str(idx) + " " + str(nb) + " " + str(tmp_idx))
            if tmp_idx < idx_left_str and tmp_idx > -1:
                idx_left_str=tmp_idx
                left_nbr_str  = str(txt_nbr[idx])
        for idx, ch in enumerate(line):
            if ch.isdigit():
                if idx < idx_left_str and idx > -1:
                    idx_left_str = idx
                    left_nbr_str = ch
                # print(ch + " " + str(idx) + " " + left_nbr_str)
        # print(left_nbr_str)

        idx_right_str = -1
        right_nbr_str = ""
        for idx, nb in enumerate(txt):
            tmp_idx = line.find(nb)
            tmp_idx_next = tmp_idx
            while tmp_idx_next != -1:
                tmp_idx_next = line.find(nb, tmp_idx_next+len(nb))
                # print(tmp_idx_next)
                if tmp_idx_next != -1:
                    tmp_idx = tmp_idx_next
            # print(str(idx) + " " + str(nb) + " " + str(tmp_idx))
            if tmp_idx > idx_right_str and tmp_idx > -1:
                idx_right_str=tmp_idx
                right_nbr_str  = str(txt_nbr[idx])
        for idx, ch in enumerate(line):
            if ch.isdigit():
                if idx > idx_right_str and idx > -1:
                    idx_right_str = idx
                    right_nbr_str = ch
        mergestr = str(left_nbr_str) +  str(right_nbr_str)
        print(str(linecounter) + ": " + mergestr + " : " + line.rstrip())
        calsum += int(mergestr)        


print(calsum)