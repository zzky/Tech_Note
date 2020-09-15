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
