# input:    ID<tab>[LABEL<tab>PROBABILITY]
# output:   ID<tab>X<tab>X<tab>LABEL
file_name = "../examen/blind_pos_es"

def main():
    text = None
    new_text = []

    with open(file_name, "r") as fr:
        text=fr.readlines() 

    for line in text: 
        blocks = line.split("\t")
        tag = ""
        prob = 0.0
        for i in range(1, 10, 2):
            try:
               if float(blocks[i+1]) > prob: 
                tag = blocks[i]
                prob = float(blocks[i+1])
            except IndexError:
                break

        new_line = "{}\tX\tX\t{}\n".format(blocks[0], tag)
        new_text.append(new_line)

    with open(file_name+"_formated", "w") as fw:
        fw.writelines(new_text)

    return

if __name__=="__main__":
    main()

