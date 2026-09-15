"""Select stable releases on default-branch pushes without evaluating commit text."""
import json,os,subprocess
from pathlib import Path

def decision(version,previous,published):
    if version==previous:return False,0,'Pack version did not change'
    if published and published['version']==version:return False,0,'Version is already published'
    return True,(published['sequence']+1 if published else 1),'Pack version changed'

def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def document(ref,path,optional=False):
    if optional:
        paths=git('ls-tree','--name-only',ref,'--',path).splitlines()
        if path not in paths:return None
    return json.loads(git('show',ref+':'+path))

def main():
    event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text());branch=event['repository']['default_branch']
    if event.get('deleted') or event['ref']!='refs/heads/'+branch:return
    current=document('HEAD','anthub.json')['pack']['version'];before=event['before'];previous=None
    if before.strip('0'):
        if subprocess.run(['git','cat-file','-e',before+'^{commit}'],capture_output=True).returncode:
            subprocess.run(['git','fetch','origin',before],check=True)
        old=document(before,'anthub.json',True);previous=old['pack']['version'] if old else None
    subprocess.run(['git','fetch','origin',branch],check=True)
    latest=document('FETCH_HEAD','anthub.json')['pack']['version']
    pointer=document('FETCH_HEAD','channels/stable.json',True)
    publish,sequence,reason=decision(current,previous,pointer)
    if latest!=current:publish=False;reason='A newer pack version is already on the default branch'
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as out:
        out.write('publish='+str(publish).lower()+'\nsequence='+str(sequence)+'\n')
    print(reason)
if __name__=='__main__':main()
