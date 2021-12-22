#!/bin/bash

# Author : CABOS Matthieu
# Date : 15/12/2021

scp mcabos@origin.srv-prive.icgm.fr:~/logwatch .
day=`date | cut -d " " -f1`
# echo $day
# day="mar."
month=`date | cut -d " " -f2`
num=`date | cut -d " " -f3`
today="$day $month $num"
# today="lun. déc. 20"
# day="lun."
# month="déc."
cut_line=`cat logwatch | grep -n "$today" | head -1 | grep -Po "\K^[0-9]+"`
nb_line=`wc -l logwatch | grep -Po "\K^[0-9]+"`
read_line=`echo $(($nb_line-$cut_line))`
Content=`cat logwatch | tail -$read_line`
Slice=""
Liste=""
CutFlag=0

for line in $Content
do
	if [ $line == $day ] && [ $CutFlag -eq 1 ]
	then
		CutFlag=0
		Liste=$Liste" "$Slice
		Slice=""
	fi
	if [ $line == $day ] || [ $line == $month ]
	then
		CutFlag=1
	fi
	if [ $CutFlag -eq 1 ]
	then
		Slice=$Slice$line
	fi
done

count=0
Liste2=""
for item in $Liste
do
	Liste2=$Liste2" "$item
	count=$((count+1))
done

IP_Slice=""
User=""
ip=""
count=1
declare -a IP_list

for item in $Liste2
do
	User=`echo $item | grep -Po "\K[A-Za-z0-9_-êïù]+@[A-Za-z0-9_-]+"`
	ip=`echo $item | grep -Po "\K([0-9]+\.){3}[0-9]+"`
	for elem in $ip  
	do
		if ! [ "$elem" == "10.14.14.20" ]
		then
			IP_Slice=$IP_Slice" ""$elem"
			ip=""
		fi
	done
	if [[ -n "$User" ]]
	then
		IP_list[$count]="$User"":""$IP_Slice"
		count=$((count + 1))
	fi
	IP_Slice=""
	User=""
done

User_IP=""
tmp=""

User=`echo ${IP_list[1]}| grep -Po "\K[A-Za-z0-9_-êïù]+@[A-Za-z0-9_-]+"`
readarray t <<<"$(echo ${IP_list[1]} $tmp | tr ' ' '\n' | sort | uniq -u)"
User_IP=$User":"${t[0]}
for i in ${!IP_list[@]}
do
	if [[ -n "$tmp" ]]
	then
		readarray t <<<"$(echo ${IP_list[$i]} $tmp | tr ' ' '\n' | sort | uniq -u)"
		User=`echo ${IP_list[$i]}| grep -Po "\K[A-Za-z0-9_-êïù]+@[A-Za-z0-9_-]+"`
		if ! [[ $User_IP = *"$User"* ]]
		then
			User_IP=$User_IP" "$User":"${t[0]}
		fi
	fi
	tmp=${IP_list[$i]}
done
for item in $User_IP
do
	echo $item
done