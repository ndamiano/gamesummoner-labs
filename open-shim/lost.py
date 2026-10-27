import json,glob,re,collections,sys,random
from math import comb
def kind(c):
    c=str(c)
    if 'carried no `code`' in c: return 'direct'
    if 'is not available here' in c and 'open()' in c: return 'open'
    if 'there is no module' in c: return 'import:'+re.search(r"no module '([^']+)'",c).group(1).split('.')[0]
    if 'not valid Python' in c: return 'syntax'
    if 'output token limit' in c: return 'cutoff'
    if re.search(r'nothing ran|nothing in the program ran',c,re.I): return 'other-refusal'
    return None
def scan(g):
    out=[]
    for f in sorted(glob.glob(g+'/transcript.json')):
        h=json.load(open(f)); h=h.get('history',h) if isinstance(h,dict) else h
        ks=[kind(m['content']) for m in h if m.get('role')=='tool' and not str(m.get('tool_call_id','')).startswith('call_seeded')]
        out.append(collections.Counter(k for k in ks if k))
    return out
def fisher(a,n1,b,n2):
    K=a+b;N=n1+n2;p=lambda x:comb(n1,x)*comb(n2,K-x)/comb(N,K);p0=p(a)
    return sum(p(x) for x in range(max(0,K-n2),min(K,n1)+1) if p(x)<=p0*1.0000001)
def perm(x,y,k=20000):
    obs=abs(sum(x)/len(x)-sum(y)/len(y));z=x+y;c=0;random.seed(1)
    for _ in range(k):
        random.shuffle(z);c+=abs(sum(z[:len(x)])/len(x)-sum(z[len(x):])/len(y))>=obs
    return c/k
