import numpy as np
column_id=np.arange(12)+2
print(column_id)
out_column_name='EMPI|Inpatient_Outpatient|Admi_Set|Prin_Set|ICD_Set \n'
fw = open("Wang_Enc_ICD.txt", 'w', encoding='utf-8')
fw.write(out_column_name)
fw.flush()
lineN=0
with open("Wang_Enc.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines()[1:]:
        contents = line.split('|')
        print(contents)
        print(lineN)
        for diag in [contents[i] for i in column_id]:
            print(diag)
        if lineN>10:
            break
        lineN+=1
'''
 out_put = "|".join([content[i] for i in file_type[item]])
                if not out_put.endswith('\n'):
                    out_put += '\n'
                out_put_file.write(out_put)
                if num % 1000 == 0:
                    print("In the file, it is going to " + str(num) + "/" + str(num_lines))
        out_put_file.flush()

'''
'''          
 for i in file_types[item]]:




    EMPIS = set()
    for item in file_type:
        with open(item + ".txt", 'r', encoding='utf-8') as f:
            
    print(len(EMPIS))

    file_types = {'Con123': [0, 6, 8], 'Dem': [4, 5, 7],
                  'Enc': [6]}
    out_put = {}
    for item in file_types.keys():
        with open(item + ".txt", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                contents = line.split('|')
                EMPI = contents[0]
                list_content = 
                if EMPI not in out_put.keys():
                    out_put[EMPI] = list_content
                else:
                    out_put[EMPI] += list_content

    for item in out_put.keys():
        list_content = out_put[item]
        out_put[item] = list(set(list_content))
    print(out_put)
'''
'''
file_type = {'Con': [0, 10, 20, 21, 22], 'Dem': [0, 8],
             'Enc': [0, 7, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]}

numOffile = 0
for item in file_type.keys():
    out_put_file = open("Wang_"+item + ".txt", 'w', encoding='utf-8')
    file_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in file_num:
        file_path0 = "../../Raw Data_diabtes/#3-0"
        target_name = 'LZ071_20181019_102004_BWH_' + item + '.txt'
        file_total_path = file_path0 + str(i) + '/' + target_name
        print("Now it is going to " + file_total_path + " of " + item)
        with open(file_total_path, 'r', encoding='utf-8') as f1:
            numOffile += 1
            lines = f1.readlines()
            num_lines = len(lines)
            for num in range(num_lines):
                content = lines[num].split('|')
                out_put = "|".join([content[i] for i in file_type[item]])
                if not out_put.endswith('\n'):
                    out_put += '\n'
                out_put_file.write(out_put)
                if num % 1000 == 0:
                    print("In the file, it is going to " + str(num) + "/" + str(num_lines))
        out_put_file.flush()
    print("Now it is going to " + str(numOffile))
    file_num.append(0)
    for i in file_num:
        file_path1 = "../../Raw Data_diabtes/#3-1"
        target_name = 'LZ071_20181019_102004_BWH_' + item + '.txt'
        file_total_path1 = file_path1 + str(i) + '/' + target_name
        print("Now it is going to " + file_total_path1 + " of " + item)
        with open(file_total_path1, 'r', encoding='utf-8') as f2:
            numOffile += 1
            lines = f2.readlines()
            num_lines = len(lines)
            for num in range(num_lines):
                content = lines[num].split('|')
                out_put = "|".join([content[i] for i in file_type[item]])
                if not out_put.endswith('\n'):
                    out_put += '\n'
                out_put_file.write(out_put)
                if num % 1000 == 0:
                    print("In the file, it is going to " + str(num) + "/" + str(num_lines))
        out_put_file.flush()
    out_put_file.close()
print("total the file num is " + str(numOffile))
'''