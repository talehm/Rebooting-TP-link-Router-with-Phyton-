    #!/bin/bash
    host=$1
    file=$2
    device=$3
    port=23
    username="admin"
    password="radmin"
    tplink="tplink"
    planet="planet"
    reboot_tplink="dev reboot"
    reboot_planet="reboot"
    date=$(date +'%d, %b %Y %I:%M:%S %p')
    echo ${file}
    ( echo open ${host} ${port}
    sleep 1
    echo ${username} 
    sleep 2
    echo ${password}
    sleep 2
    echo  "${date} ${device}: Logged In" >> ${file}
    echo ${reboot_tplink}
    echo ${reboot_planet}
    sleep 3
    echo exit ) | telnet

