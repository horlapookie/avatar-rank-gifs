"""Save generated GIFs with GitHub's REST API, without git shell commands."""
import base64, concurrent.futures, json, os, time
from pathlib import Path
import requests

repo=os.environ['GITHUB_REPOSITORY']
token=os.environ['GH_TOKEN']
base='https://api.github.com/repos/'+repo
headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
def api(method,path,data=None):
    for attempt in range(5):
        response=requests.request(method,base+path,headers=headers,json=data,timeout=120)
        if response.status_code in (429,502,503,504):
            time.sleep(int(response.headers.get('Retry-After','10'))*(attempt+1))
            continue
        if not response.ok:
            raise RuntimeError(f'GitHub {response.status_code}: {response.text}')
        return response.json()
    raise RuntimeError('GitHub temporary failure after retries')
ref=api('GET','/git/ref/heads/main')
parent=ref['object']['sha']
commit=api('GET','/git/commits/'+parent)
files=sorted(Path('gifs').glob('*'))
assert len(list(Path('gifs').glob('*.gif')))==69

def blob(path):
    result=api('POST','/git/blobs',{'content':base64.b64encode(path.read_bytes()).decode(),'encoding':'base64'})
    print('Saved '+str(path),flush=True)
    return {'path':str(path),'mode':'100644','type':'blob','sha':result['sha']}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    entries=list(pool.map(blob,files))
tree=api('POST','/git/trees',{'base_tree':commit['tree']['sha'],'tree':entries})
new_commit=api('POST','/git/commits',{'message':'Add all 69 verified five-second rank and promotion GIFs','tree':tree['sha'],'parents':[parent]})
api('PATCH','/git/refs/heads/main',{'sha':new_commit['sha'],'force':False})
result=api('GET','/git/trees/'+new_commit['sha']+'?recursive=1')
count=sum(entry['path'].endswith('.gif') for entry in result['tree'])
assert count==69, count
print('Confirmed all 69 GIFs are committed on main.',flush=True)
