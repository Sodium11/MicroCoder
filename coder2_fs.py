from microbit import *
display.show("S")
mode = ""
instructions=['M','+','-',':','J','Z','G','L','R']
registers=['a','b','c','d','I','O']
label=['A','B','C']
#display.scroll("A:NEW B:OPEN")

#main menu START
#A:make a new program
#B:open the saved program
while True:
    if (button_a.was_pressed()):
        mode = "NEW"
        break
    if (button_b.was_pressed()):
        mode = "OPEN"
        break
display.scroll(mode)
#main menu END

#file system START
if(mode=="OPEN"):
    #file select START
    file_sel=0
    while(not button_b.was_pressed()):
        display.show(file_sel)
        if(button_a.was_pressed()):
            file_sel+=1
            if(file_sel>9):
                file_sel=0
    file_name=str(file_sel)+".mbc"
    #file select END
    file=open(file_name,"r")
    program=file.read()
    file.close()
    for ch in program:
        display.show(ch)
        sleep(500)
        if button_a.was_pressed():
            break
    mode="RUN"
#file system END
if(mode=="NEW"):
    program=""
    n=0
    input_done=0
    while input_done==0:
        display.show(instructions[n])
        if button_a.was_pressed():
            n+=1
            if n>=len(instructions):
                n=0

        if button_b.was_pressed():
            if (instructions[n]=='R'):
                input_done=1
                display.scroll(program)
                continue
            program+=instructions[n]
            #2 ope
            if (instructions[n] == 'M' or instructions[n] == '+' or instructions[n] == '-'):
                sel_1=0
                sel_2=0
                #A select
                while not button_b.was_pressed():
                    display.show(registers[sel_1])
                    if button_a.was_pressed():
                        sel_1+=1
                        if sel_1>=len(registers):
                            sel_1=0
            #B select
                while not button_b.was_pressed():
                    display.show(registers[sel_2])
                    if button_a.was_pressed():
                        sel_2+=1
                        if sel_2>=len(registers):
                            sel_2=0
                program+=(registers[sel_1]+registers[sel_2])
            #1 ope
            if (instructions[n] == ':'):
                sel=0
                while not button_b.was_pressed():
                    display.show(label[sel])
                    if button_a.was_pressed():
                        sel+=1
                        if sel>=len(label):
                            sel=0
                program+=label[sel]

            if (instructions[n] == 'J' or instructions[n] == 'Z' or instructions[n] == 'G' or instructions[n] == 'L'):
                sel=0
                while not button_b.was_pressed():
                    display.show(label[sel])
                    if button_a.was_pressed():
                        sel+=1
                        if sel>=len(label):
                            sel=0
                program+=label[sel]
                if(instructions[n]!='J'):
                    sel=0
                    while not button_b.was_pressed():
                        display.show(registers[sel])
                        if button_a.was_pressed():
                            sel+=1
                            if sel>=len(registers):
                                sel=0
                    program+=registers[sel]
    display.scroll("SAVE")
    file_sel=0
    while(not button_b.was_pressed()):
        display.show(file_sel)
        if(button_a.was_pressed()):
            file_sel+=1
            if(file_sel>9):
                file_sel=0
    file_name=str(file_sel)+".mbc"
    file=open(file_name,"w")
    file.write(program)
    file.close()
    mode="RUN"

if mode=="RUN":
    display.scroll("R")
    #running code
    label_map=[]
    for i in range(len(label)):
        label_map.append(-1)
    #label check
    for i in range(len(program)):
        if program[i] == ':':
            l=program[i+1]
            label_map[label.index(l)]=i+2


    pointer=0
    p_end=0
    #registers preparation
    registers_data=[]
    for i in range(len(registers)):
        registers_data.append(0)

    while p_end==0 and pointer<len(program):
        opecode=program[pointer]
        #opecode MOVE
        if opecode=='M':
            first=program[pointer+1]
            second=program[pointer+2]
            if (first=='I'):#input
                I_done=0
                I_num=1
                I_str=""
                while I_done==0:
                    if I_num==10:
                        display.show(";")
                    else:
                        display.show(str(I_num))
                    if button_a.was_pressed():
                        I_num+=1
                        if I_num>10:
                            I_num=0
                    if button_b.was_pressed():
                        if I_num<10:
                            I_str+=str(I_num)
                            continue
                        elif I_num==10:
                            if len(I_str)==0:
                                display.scroll("INPUT!")
                                continue
                            registers_data[registers.index(second)]=int(I_str)
                            I_done=1
            elif (second=='O'):#output
                display.scroll(str(registers_data[registers.index(first)]))
            else:
                registers_data[registers.index(second)]=registers_data[registers.index(first)]
        #opecode ADD & SUB
        if opecode=='+':
            first_p=registers.index(program[pointer+1])
            second_p=registers.index(program[pointer+2])
            registers_data[second_p]+=registers_data[first_p]
        if opecode=='-':
            first_p=registers.index(program[pointer+1])
            second_p=registers.index(program[pointer+2])
            registers_data[second_p]-=registers_data[first_p]
        #opecode JUMP
        if opecode=='J':
            pointer=label_map[label.index(program[pointer+1])]
            continue
        if opecode=='Z':
            second_p=registers.index(program[pointer+2])
            data=registers_data[second_p]
            if data == 0:
                pointer=label_map[label.index(program[pointer+1])]
                continue
        if opecode=='G':
            second_p=registers.index(program[pointer+2])
            data=registers_data[second_p]
            if data > 0:
                pointer=label_map[label.index(program[pointer+1])]
                continue
        if opecode=='L':
            second_p=registers.index(program[pointer+2])
            data=registers_data[second_p]
            if data < 0:
                pointer=label_map[label.index(program[pointer+1])]
                continue
        pointer+=1