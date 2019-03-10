from microbit import *
mode = ""
#display.scroll("A:NEW B:OPEN")
display.show("C")
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
            if(file_sel>2):
                file_sel=0
    file_name=str(file_sel)+".bf"
    #file select END
    file=open(file_name,"r")
    program=file.read()
    file.close()
    display.scroll(program)
    mode="RUN"
#file system END


if(mode=="NEW"):
    
    inst_n=0
    instructions=['+','-','>','<','[',']','.','R']
    program=""
    while True:
    #operation select menu START
        if button_a.was_pressed():
            inst_n+=1
        if(inst_n>7):
            inst_n=0
        display.show(instructions[inst_n])
    #operation select menu END

        if button_b.was_pressed():
            if instructions[inst_n]!='R':
                program+=instructions[inst_n]
            else:
                file_sel=0
                while(not button_b.was_pressed()):
                    display.show(file_sel)
                    if(button_a.was_pressed()):
                        file_sel+=1
                        if(file_sel>2):
                            file_sel=0
                file_name=str(file_sel)+".bf"
                file=open(file_name,"w")
                file.write(program)
                file.close()
                mode="RUN"
        if(mode=="RUN"):
            break

if(mode=="RUN"):
    mode=""
    #execution START
    display.show(" ")
    memory=[]
    for i in range(100):#100 cells
        memory.append(0)
    #display.scroll(program)
    pp=0#program pointer
    mp=0#memory pointer
    while True:
        ope=program[pp]
        if(ope=='+'):
            memory[mp] += 1
        elif(ope=='-'):
            memory[mp]-=1
        elif(ope=='>'):
            mp+=1
        elif(ope=='<'):
            mp-=1
        elif(ope=='['):
            if (memory[mp]==0):
                ignore=0
                pp+=1
                while True:
                    if(program[pp]=='['):
                        ignore+=1
                    elif(program[pp]==']'):
                        ignore-=1
                    pp+=1
                    if (program[pp]==']' and ignore==0):
                        break
        elif(ope==']'):
            if (memory[mp]!=0):
                ignore=0
                pp-=1
                while True:
                    if(program[pp]==']'):
                        ignore+=1
                    elif(program[pp]=='['):
                        ignore-=1
                    pp-=1
                    if (program[pp]=='[' and ignore==0):
                        break

        elif(ope=='.'):
            #while(not button_a.is_pressed()):
            #    display.show("O")
            display.scroll(str(memory[mp]))
                
        pp+=1
        if pp>=len(program):
            break
        #execution END