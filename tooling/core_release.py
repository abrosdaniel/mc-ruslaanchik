"""Build a signed official AntHub descriptor; never publish or generate private keys."""
import argparse
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from anthub import encoded,sha,sign,write,validate_schema
p=argparse.ArgumentParser();p.add_argument('--jar',type=Path,required=True);p.add_argument('--url',required=True);p.add_argument('--version',required=True);p.add_argument('--sequence',type=int,required=True);p.add_argument('--key',type=Path,required=True);p.add_argument('--key-id',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--minecraft',default='1.21.1');p.add_argument('--neoforge',default='21.1.250');a=p.parse_args()
artifact=a.jar.read_bytes();descriptor=dict(schemaVersion=1,version=a.version,sequence=a.sequence,artifacts=[dict(minecraft=a.minecraft,neoForge=a.neoforge,java=21,url=a.url,sha256=sha(artifact),size=len(artifact),helperProtocolVersion=1)])
validate_schema('core-release',descriptor);key=serialization.load_pem_private_key(a.key.read_bytes(),password=None);a.output.mkdir(parents=True,exist_ok=True);write(a.output/'core.json',descriptor);write(a.output/'core.json.sig.json',sign(encoded(descriptor),key,a.key_id))
print('Signed official descriptor created')
