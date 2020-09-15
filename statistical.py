file_type=['Con123','Dem','Enc']
EMPIS=set()
for item in file_type:
    with open(item + ".txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            contents=line.split('|')
            EMPI=contents[0]
            EMPIS.add(EMPI)
print(len(EMPIS))

file_types = {'Con123': [0,6,8], 'Dem': [4,5,7],
             'Enc': [6]}
out_put={}
for item in file_types.keys():
    with open(item + ".txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            contents=line.split('|')
            EMPI=contents[0]
            list_content=[contents[i] for i in file_types[item]]
            if EMPI not in out_put.keys():
                out_put[EMPI]=list_content
            else:
                out_put[EMPI] += list_content

for item  in out_put.keys():
    list_content=out_put[item]
    out_put[item]=list(set(list_content))
print(out_put)

