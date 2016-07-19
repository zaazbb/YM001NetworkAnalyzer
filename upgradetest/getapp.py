
start_flag = '========'.encode()
end_flag = '========'.encode()

with open('untitle.txt', 'rb') as f, open('app.bin', 'wb') as fo:
    d = f.read()
    start = d.index(start_flag)
    print(hex(start))
    end = d.rindex(end_flag)
    print(hex(end))
    fo.write(d[start+len(start_flag):end])
    
