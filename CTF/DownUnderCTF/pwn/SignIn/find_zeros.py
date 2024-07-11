from pwn import u64, p64
# gdb.attach(conn, 'dump binary memory mem.bin 0x400000 0x405000')
# To dump memory

data = open('mem.bin', 'rb').read()
qwords = [u64(data[i:i+8]) for i in range(0, len(data), 8)]
for i, qw in enumerate(qwords):
    if 0x400000 <= qw <= 0x405000:
        idx = (qw - 0x400000)//8
        if qwords[idx] == 0:
            print('ok!', hex(0x400000 + 8*i))

