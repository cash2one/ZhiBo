#!/bin/bash

if [ -f ~/.bash_profile ];
then
    . ~/.bash_profile
fi

echo "starting jhssd" >>/root/ming/webserver/SEMain/liming
nohup python /root/ming/webserver/SEMain/app.py >/root/ming/webserver/SEMain/newLog 2>&1 &
