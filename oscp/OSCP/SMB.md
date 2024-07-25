 - Setup smb share between kali and windows
```
# To recap, I used this command in Kali while in the kali user home drive:
impacket-smbserver <custom SMB drive name> . -smb2support

# On the Windows machine, I opened PowerShell as administrator and ran:
net use \\<Kali VM IP address>\<custom SMB drive name>

# After running those commands, I opened Run and entered:
\\<Kali VM IP address>\<chosen SMB drive name> 
```













