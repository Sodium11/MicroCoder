from microbit import *
inst_n=0
instructions=['+','-','>','<','[',']','.','R']
program=""
memory=[]
for i in range(100):#100 cells
    memory.append(0)
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
            #execution START
            #display.scroll(program)
            pp=0#program pointer
            mp=0#memory pointer
            while True:
                ope=program[pp]
                if(ope=='+'):
                    memory[mp]+=1
                if(ope=='-'):
                    memory[mp]-=1
                if(ope=='>'):
                    mp+=1
                if(ope=='<'):
                    mp-=1
                if(ope=='['):
                    if (memory[mp]==0):
                        ignore=0
                        pp+=1
                        while True:
                            if(program[pp]=='['):
                                ignore+=1
                            if(program[pp]==']'):
                                ignore-=1
                            pp+=1
                            if (program[pp]==']' and ignore==0):
                                break
                if(ope==']'):
                    if (memory[mp]!=0):
                        ignore=0
                        pp-=1
                        while True:
                            if(program[pp]==']'):
                                ignore+=1
                            if(program[pp]=='['):
                                ignore-=1
                            pp-=1
                            if (program[pp]=='[' and ignore==0):
                                break

                if(ope=='.'):
                    #while(not button_a.is_pressed()):
                    #    display.show("O")
                    display.scroll(str(memory[mp]))
                
                pp+=1
                if pp>=len(program):
                    break
                #execution END