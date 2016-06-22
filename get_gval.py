
import pprint


with open(r'D:\work\repository\YM001\trunk\software\proj\app\obj\app.M51') as f:
    global_area = False
    module = ''
    gvar = []
    for line in f:
        if line.startswith('  -------         MODULE'):
            module = line.rsplit(maxsplit=1)[-1]
            if module[0] != '?':
                global_area = True
        elif line.startswith('  X:'):
            if global_area:
                attr = line.rsplit()
                if attr[2][0] != '?':
                    gvar.append([attr[2], int(attr[0][2:-1], 16), 0, attr[1], module])
        elif line.startswith('  -------         PROC') \
             or line.startswith('  -------         ENDMOD'):
            global_area = False
print('finished.')
pprint.pprint(gvar)


gvar_by_addr = sorted(gvar, key=lambda d:d[1])
pprint.pprint(gvar_by_addr)
for i in range(len(gvar_by_addr)-1):
    gvar_by_addr[i][2] = gvar_by_addr[i+1][1] - gvar_by_addr[i][1]
gvar_by_addr[-1][2] = 0x8000 - gvar_by_addr[-1][1]

pprint.pprint(gvar_by_addr)
pprint.pprint(sorted(gvar_by_addr, key=lambda d:d[0]))
