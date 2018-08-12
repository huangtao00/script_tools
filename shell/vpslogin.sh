#!/usr/bin/env bash
username=root
password="xxxx"
ip=45.76.194.104
package=blog-all-`date +%-Y%m-%d`.tar.gz
blogpath="/root/script"

/usr/bin/expect <<-EOF
set timeout 50
spawn ssh ${username}@${ip}
expect {
"*yes/no" { send "yes\r"; exp_continue }
"*password:" { send "$password\r" }
}
expect "*#"
send "pwd\r"
expect "*#"
send  "cd /root/script\r"
expect "*#"
send  "pwd\r"
expect "*#"
# send "./backupblog.sh\r"
# expect "*#"
send "exit\r"
expect "logout"
expect "$"


# spawn scp -r ${username}@${ip}:${blogpath}/${package} ${package}
# expect {
# "*yes/no" { send "yes\r"; exp_continue }
# "*password:" { send "$password\r" }
# }
# expect "100%"
# expect "$"


spawn ssh ${username}@${ip}
expect {
"*yes/no" { send "yes\r"; exp_continue }
"*password:" { send "$password\r" }
}
expect "*#"
send  "cd /root/script\r"
expect "*#"
send "mv -f *.tar.gz  backup\r"
expect "*#"
send "exit\r"
expect eof
EOF
