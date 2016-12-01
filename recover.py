#!/usr/bin/env python

import sys, pgp
from pgp import constants as c
from Crypto.Signature.PKCS1_v1_5 import EMSA_PKCS1_V1_5_ENCODE
from Crypto.Util.number import long_to_bytes, bytes_to_long

print("[i] loading pgp data", file=sys.stderr)
raw=sys.stdin.buffer.read()
packets=list(pgp.packets.parsers.parse_binary_packet_data(raw))[0]
if(isinstance(packets, pgp.packets.packets.CompressedDataPacket)):
    print('[i] compressed pgp data, decompressing', file=sys.stderr)
    packets = packets.decompress_data(packets.compression_algorithm, packets.compressed_data)
msg = None
sig = None
for p in packets:
    if(isinstance(p, pgp.packets.packets.LiteralDataPacket)):
        print("[i] found signed data", file=sys.stderr)
        msg=packets[1].data
    elif(isinstance(p,pgp.packets.packets.SignaturePacket)):
        if(not p.public_key_algorithm in [c.PUBKEY_ALGO_RSA, c.PUBKEY_ALGO_RSA_S]): continue
        print("[i] found signature", file=sys.stderr)
        sig=True
if not msg:
    print("[!] dang, couldn't find signed data, bailing out", file=sys.stderr)
    sys.exit(1)
if not sig:
    print("[!] dang, couldn't find signature, bailing out", file=sys.stderr)
    sys.exit(1)

_sig=pgp.open_pgp_message_from_packets(packets).signatures
if(len(_sig)!=1):
    print("[!] dang more than one signature found, bailing out", file=sys.stderr)
    sys.exit(1)
_sig=_sig[0]
sig=_sig.signature_values[0]

print("[i] hashing message&metadata", file=sys.stderr)
hash_ = pgp.utils.get_hash_instance(_sig.hash_algorithm)
hash_.update(msg)
hash_.update(_sig.to_signable_data(_sig.signature_type, _sig.version))
paddedhash=EMSA_PKCS1_V1_5_ENCODE(hash_, 512)
m=bytes_to_long(paddedhash)
print(sig, m)
print("[.] done extracting msg and sig from pgp data", file=sys.stderr)
# calculate (sig^65537-m) for both messages and then gcd the results
#     gcd(sig1^65537-m1, sig2^65537-m2)
