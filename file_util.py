def splitter():
    with open('testaf.txt', 'r') as testaf:
        for i in range(1, 20):
            counter = 0
            with open('output' + str(i) + '.txt', 'a+') as output:
                while counter < 10000:
                    line = testaf.next()
                    print line
                    output.write(line)
                    counter += 1

def joiner():
    with open('onethroughnineteen.txt', 'a+') as outputfinal:
        for i in range(1, 20):
            with open('super_output' + str(i) + '.txt', 'r') as chunk:
                outputfinal.writelines(chunk.readlines())
