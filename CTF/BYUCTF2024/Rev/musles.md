# Musles 
https://github.com/BYU-CSA/BYUCTF-2024-Public

Description:  
```
Here's another binary to test your rev musles!! Let's see how you do :)

[musles]
```
### Writeup
This is a binary that uses musl instead of libc. It creates a new section of memory, writes encrypted shellcode to it, XORs it with a constant, and then runs the shellcode that will read in a flag and compare it to the correct flag.  

Flag - byuctf{ur_GDB_skills_are_really_swoll}  

To start, this binary uses musl, not libc. Trying to run the binary on a kali vm resulted in an error. Some googling showed that Alpine linux uses musl so I created a VM which was overkill, but the binary ran. Using a docker container is a better choice. The **Dockerfile** I used to build the container is as follows: 

```
# Use Alpine Linux as the base image
FROM alpine:latest

# Update package index and install GDB
RUN apk update && \
    apk add --no-cache gdb && \
    apk add --no-cache binutils
```

Build and run this container to include the binary: 
```
$ sudo docker build -t alpine-gdb .
$ sudo docker run -it --rm -v ~/Downloads/rev/musles:/usr/bin/musles alpine-gdb
```

File: 
```
musles: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-x86_64.so.1, stripped
```

Another important note is the binary is an position independent executable (pie). It is also stripped, so no symbols. I could not initially generate the assembly in **gdb** so I used **objdump -d** to get disassembly. This gave me an idea of what was going on. Note, when running the binary there is a time out with an output along the lines of "Alarm". When inspecting the disassembly from **objdump** we can see there is a call to alarm. This will have to be avoided or patched. In **gdb** I was able to place a breakpoint on **__libc_start_main** which allows the addresses to be determined and from here a breakpoint can be placed on **main**.   

Key functions in main include:  
- **mmap** which creates a new mapping in the virtual address space of the calling process. 
- **system** which closes out the process
- **memcpy** which copies encrypted shell code into the virtual address space created by **mmap**
- **alarm** responsible for the timeout of the program

The **alarm** call needs to be patched.
```
set *<addr>=0x90
```

Then, there are multiple calls to **exit** that need to be avoided. I used **jump** to get around these: 
```
jump *<addr>
```

After memcpy, there is a call to ***rax** which needs to be stepped into. From here the two values being placed in the registers need to be xored and decoded. The decoding can be done in the following way: 

```python
v1 = 0xf3cf3f9d7b8743e3
...
v10 = 0x6990ab8c0bb5

r1 = v1 ^ v2
...
r5 = v9 ^ v10

# Convert the integer to bytes
bs1 = int.to_bytes(r1, length=8, byteorder='little')
...
bs5 = int.to_bytes(r5, length=8, byteorder='little')

# Decode the bytes as ASCII
s1 = bs1.decode('ascii')
...
s5 = bs5.decode('ascii')

print(s1 + s2 + s3 + s4 + s5)
```

Done. 