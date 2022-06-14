
file_name = "../gender_ca/training_gender_ca"
# file_name = "/home/fran/muiinf/sin/parte2/maxima_entropia/stance_and_gender_detection/scripts/prueba"

def main():
    text = None
    new_text = []

    with open(file_name, "r") as fr:
        text=fr.readlines() 

    for line in text: 
        blocks = line.split("\t")
        new_line = blocks[0] + "\t" + blocks[1] + "\t" 
        for word in blocks[2].split(" "):
            if not "http" in word:
                new_line += word + " "
            else:
                if "\n" in word:
                    new_line += "\n"
        new_line = new_line.removesuffix(" ")
        new_text.append(new_line)

    with open(file_name+"_noURLs", "w") as fw:
        fw.writelines(new_text)

    return

if __name__=="__main__":
    main()
