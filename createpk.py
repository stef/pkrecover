#!/usr/bin/env python

import sys, os
from pgp.packets import packets
from pgp import constants as c

print("[i] assembling new public key", file=sys.stderr)

#pkp=PublicKeyPacket(header_type, version, creation_time,
#                 public_key_algorithm, expiration_days=None, modulus=None,
#                 exponent=None, prime=None, group_order=None,
#                 group_generator=None, key_value=None)
pkp=packets.PublicKeyPacket(c.OLD_PACKET_HEADER_TYPE, 4, 0, c.PUBKEY_ALGO_RSA,
                            modulus=int(sys.argv[1]), exponent=65537)
fp = os.fdopen(sys.stdout.fileno(), 'wb')
fp.write(bytes(pkp))
