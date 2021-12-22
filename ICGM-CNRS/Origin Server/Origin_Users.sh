ssh origin.srv-prive.icgm.fr

#Liste utilisateurs :

/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"

cat /usr/local/flexlm/orglabdebug.log

#Numero de port

netstat -anp | grep ':::*' | grep LISTEN | cut -d ":" -f4 > tmp
sort -n tmp | tail -1                                                # Numero de port
rm tmp

#Liste Ip Utilisateurs

ss -n -t | grep <numero de port>  > tmp
cat tmp | grep -Po "\K([0-9]*\.){3}[0-9]+"  # Prendre 1 @ sur 2

#Liste Hostname Utilisateurs

ss -n -t -r | grep 60213 | cut -d " " -f16

# Liste @MAC

read Ordinateurs.ods
if host==host
	recuperer @mac
	recuperer DPT

ssh Balard-1D-1 < tmp.sh > test.txt


connexion dans l'ordre

netstat -n -t