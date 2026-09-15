#!/usr/bin/env python3
"""AntHub project validation, immutable lock building and Ed25519 signatures."""
import argparse, base64, datetime, hashlib, json, os, re, shutil, socket, ipaddress, urllib.request, urllib.parse
from pathlib import Path
from jsonschema import Draft202012Validator
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

SCHEMAS=Path(__file__).resolve().parents[1]/'schemas/v1'
def pairs(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('Duplicate JSON key: '+k)
        d[k]=v
    return d
def read(p):return json.loads(Path(p).read_text(),object_pairs_hook=pairs)
def encoded(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def write(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_bytes(encoded(o))
def validate_schema(name,o):Draft202012Validator(read(SCHEMAS/(name+'.schema.json'))).validate(o)
def sha(b):return hashlib.sha256(b).hexdigest()
def pathcheck(p):
    roots={'mods','config','defaultconfigs','kubejs','resourcepacks','shaderpacks'}
    parts=p.split('/')
    if len(parts)<2 or parts[0] not in roots or any(x in p for x in ('\\',':')) or any(ord(c)<32 for c in p):raise ValueError('Unsafe path: '+p)
    if any(x in ('','.','..') or x.endswith(('.', ' ')) or re.fullmatch(r'(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?',x,re.I) for x in parts):raise ValueError('Unsafe segment: '+p)
    if parts[0]=='config' and parts[1].lower().startswith('anthub'):raise ValueError('Protected config: '+p)
def semantics(components,files,servers):
    ids={c['id']:c for c in components}
    if len(ids)!=len(components):raise ValueError('Duplicate component id')
    def closure(initial):
        result=set();visiting=set()
        def walk(i):
            if i in visiting:raise ValueError('Dependency cycle: '+i)
            if i in result:return
            if i not in ids:raise ValueError('Missing dependency: '+i)
            visiting.add(i)
            for dep in ids[i]['dependencies']:walk(dep)
            visiting.remove(i);result.add(i)
        for i in initial:walk(i)
        for i in result:
            for other in ids[i]['conflicts']:
                if other not in ids:raise ValueError('Missing conflict: '+other)
                if other in result:raise ValueError('Conflicting selection: '+i+'/'+other)
        return result
    required={c['id'] for c in components if c['kind']=='required'}
    closure(required)
    for i in ids:closure(required|{i})
    paths=set()
    for f in files:
        pathcheck(f['path']);key=f['path'].casefold()
        if key in paths:raise ValueError('Duplicate path: '+key)
        paths.add(key)
        if f['componentId'] not in ids:raise ValueError('Missing component')
        if f['path'].startswith('mods/') and f['policy']!='enforce':raise ValueError('Mods must enforce')
    if len({s['id'] for s in servers})!=len(servers):raise ValueError('Duplicate server id')
    if len({s['address'].lower() for s in servers})!=len(servers):raise ValueError('Duplicate server address')
def load_project(root):
    p=read(root/'anthub.json');validate_schema('project',p)
    source=(root/p['pack']['manifest']).resolve()
    if not source.is_relative_to(root.resolve()):raise ValueError('Pack manifest path escapes repository')
    c=read(source);validate_schema('client-pack',c)
    fs=[dict(f,componentId=x['id']) for x in c['components'] for f in x['files']]
    semantics(c['components'],fs,p['servers'])
    if 'defaultServerId' in p and p['defaultServerId'] not in {s['id'] for s in p['servers']}:raise ValueError('Unknown defaultServerId')
    return p,c,fs
class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        check_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def check_url(url):
    u=urllib.parse.urlparse(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('Public HTTPS required')
    for a in socket.getaddrinfo(u.hostname,u.port or 443):
        if not ipaddress.ip_address(a[4][0]).is_global:raise ValueError('Private download address rejected')
def download(url):
    check_url(url)
    with urllib.request.build_opener(Redirects()).open(url,timeout=30) as response:
        data=response.read(512*1024*1024+1)
        if len(data)>512*1024*1024:raise ValueError('Tooling download limit 512 MiB exceeded')
        return data
def public(key,key_id):return {'schemaVersion':1,'keyId':key_id,'algorithm':'Ed25519','publicKey':base64.b64encode(key.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)).decode()}
def sign(data,key,key_id):return {'schemaVersion':1,'keyId':key_id,'algorithm':'Ed25519','signature':base64.b64encode(key.sign(data)).decode()}
def build(args):
    root=args.project.resolve();p,c,files=load_project(root);out=args.output;out.mkdir(parents=True,exist_ok=True)
    if (out/'anthub.lock.json').exists():raise ValueError('Output already contains a lock; use a fresh output directory')
    repo=args.repository.rstrip('/').removesuffix('.git').lower()
    if not re.fullmatch(r'https://github.com/[a-z0-9_.-]+/[a-z0-9_.-]+',repo):raise ValueError('Expected GitHub repository URL')
    release_url=repo+'/releases/download/pack-v'+p['pack']['version']+'/'
    locked=[]
    for f in files:
        f=dict(f);expected=f.pop('sha256',None)
        if 'repositoryPath' in f:
            path=(root/f.pop('repositoryPath')).resolve()
            if not path.is_relative_to(root):raise ValueError('Repository source escapes root')
            data=path.read_bytes();asset=sha(data);(out/asset).write_bytes(data);f['url']=release_url+asset
        else:data=download(f['url'])
        if expected and sha(data)!=expected:raise ValueError('Source hash changed: '+f['path'])
        f.update(sha256=sha(data),size=len(data));locked.append(f)
    content=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.relative_to(root).parts[0] not in ('content','assets'):continue
        data=path.read_bytes();asset=sha(data);(out/asset).write_bytes(data);rel=path.relative_to(root).as_posix()
        kind='asset' if rel.startswith('assets/') else ('news' if '/news/' in rel else ('rules' if path.stem=='rules' else 'changelog'))
        content.append(dict(id=rel,type=kind,url=release_url+asset,sha256=asset,size=len(data)))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    lock={k:v for k,v in p.items() if k not in ('pack','content')}
    lock['project']=dict(p['project'],repository=repo)
    lock.update(release=dict(version=p['pack']['version'],channel=args.channel,sequence=args.sequence,createdAt=now,sourceCommit=args.commit,updatePolicy=args.policy),components=[{k:v for k,v in x.items() if k!='files'} for x in c['components']],files=locked,content=content)
    validate_schema('lock',lock);semantics(lock['components'],locked,p['servers'])
    key=serialization.load_pem_private_key(args.key.read_bytes(),password=None)
    if not isinstance(key,Ed25519PrivateKey):raise ValueError('Ed25519 key required')
    data=encoded(lock);(out/'anthub.lock.json').write_bytes(data);write(out/'anthub.lock.sig.json',sign(data,key,args.key_id))
    pointer=dict(schemaVersion=1,repository=repo,channel=args.channel,sequence=args.sequence,version=p['pack']['version'],lockUrl=release_url+'anthub.lock.json',lockSha256=sha(data),signatureUrl=release_url+'anthub.lock.sig.json',publishedAt=now)
    write(out/(args.channel+'.json'),pointer);write(out/(args.channel+'.sig.json'),sign(encoded(pointer),key,args.key_id))
    print('Built signed release',p['pack']['version'],sha(data))
def main():
    a=argparse.ArgumentParser();sub=a.add_subparsers(dest='command',required=True)
    verify=sub.add_parser('verify-release');verify.add_argument('release',type=Path);verify.add_argument('--public-key',type=Path,required=True)
    v=sub.add_parser('validate');v.add_argument('project',type=Path)
    k=sub.add_parser('keygen');k.add_argument('--private',type=Path,required=True);k.add_argument('--public',type=Path,required=True);k.add_argument('--key-id',default='project-1')
    b=sub.add_parser('build-lock');b.add_argument('project',type=Path);b.add_argument('--output',type=Path,required=True);b.add_argument('--repository',required=True);b.add_argument('--commit',required=True);b.add_argument('--sequence',type=int,required=True);b.add_argument('--channel',choices=['stable','beta','dev'],default='stable');b.add_argument('--policy',choices=['required','recommended'],default='recommended');b.add_argument('--key',type=Path,required=True);b.add_argument('--key-id',default='project-1')
    args=a.parse_args()
    if args.command=='validate':load_project(args.project);print('Project valid')
    elif args.command=='build-lock':build(args)
    elif args.command=='verify-release':
        raw=(args.release/'anthub.lock.json').read_bytes();lock=read(args.release/'anthub.lock.json');validate_schema('lock',lock)
        sig=read(args.release/'anthub.lock.sig.json');key=read(args.public_key);validate_schema('signature',sig);validate_schema('public-key',key)
        if sig['keyId']!=key['keyId']:raise ValueError('Signature key identity mismatch')
        public_key=serialization.load_der_public_key(base64.b64decode(key['publicKey']));public_key.verify(base64.b64decode(sig['signature']),raw)
        semantics(lock['components'],lock['files'],lock['servers']);print('Release signature and manifest valid')
    else:
        if args.private.exists() or args.public.exists():raise ValueError('Refusing to replace existing signing key')
        key=Ed25519PrivateKey.generate();args.private.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(args.private,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb') as f:f.write(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        write(args.public,public(key,args.key_id));print('Signing key generated; private key must remain secret')
if __name__=='__main__':main()
