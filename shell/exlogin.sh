#!/usr/bin/expect
set timeout 50
# spawn "./loginjpan.sh"
 set username root
 set ip 45.76.194.104
set password  "yourpassword"
spawn ssh ${username}@${ip}
expect "*password:"  {send "$password\r"}
expect "Last login:"
send "pwd\r"
interact
