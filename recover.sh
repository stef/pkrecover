#!/bin/bash
set -e
echo "[+] processing 1st signed data" >&2
sm1=$(cat $1 | python3 ./recover.py)
echo "[+] processing 2nd signed data" >&2
sm2=$(cat $2 | python3 ./recover.py)
echo "[+] doing math magic" >&2
gcd=$(./gcd $sm1 $sm2)
python3 ./createpk.py $gcd

