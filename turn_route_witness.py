"""Find a minimum-cost route subject to explicit consecutive-edge restrictions."""
import argparse, json, pathlib, sys

def need(ok, message):
    if not ok: raise ValueError(message)

def integer(n, low=0, high=10**9):
    need(type(n) is int and low <= n <= high, 'integer outside supported range')
    return n

def ident(s):
    need(type(s) is str and 0 < len(s) <= 80, 'invalid identifier')
    return s

def fields(obj, required, optional=()):
    need(type(obj) is dict and set(required) <= set(obj) <= set(required)|set(optional), 'missing or unknown fields')

def unique_pairs(pairs):
    out={}
    for k,v in pairs:
        need(k not in out, 'duplicate JSON key')
        out[k]=v
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=pathlib.Path);a=p.parse_args()
    try:
        with a.input.open('rb') as f: raw=f.read(1048577)
        need(len(raw) <= 1048576, 'input exceeds 1 MiB')
        doc=json.loads(raw.decode('utf-8'),object_pairs_hook=unique_pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
        out=analyze(doc);print(json.dumps(out,ensure_ascii=True,sort_keys=True));return out.get('exit_code',0)
    except (ValueError,OSError,UnicodeError,RecursionError,OverflowError) as e:
        print(str(e),file=sys.stderr);return 2


import heapq

def analyze(doc):
    fields(doc,('nodes','edges','forbidden','start','end'))
    need(type(doc['nodes']) is list and 1<=len(doc['nodes'])<=200,'expected 1..200 nodes');nodes=[ident(x) for x in doc['nodes']]
    need(len(set(nodes))==len(nodes),'duplicate node');nodes=set(nodes);start,end=ident(doc['start']),ident(doc['end']);need(start in nodes and end in nodes,'unknown endpoint')
    need(type(doc['edges']) is list and len(doc['edges'])<=1000,'too many edges');edges={};out={n:[] for n in nodes}
    for e in doc['edges']:
        fields(e,('id','from','to','cost'));k,a,b=ident(e['id']),ident(e['from']),ident(e['to']);c=integer(e['cost'])
        need(k not in edges and a in nodes and b in nodes,'duplicate edge or unknown node');edges[k]=(a,b,c);out[a].append(k)
    need(type(doc['forbidden']) is list and len(doc['forbidden'])<=5000,'too many restrictions');banned=set()
    for turn in doc['forbidden']:
        need(type(turn) is list and len(turn)==2,'turn must contain two edge IDs');a,b=map(ident,turn)
        need(a in edges and b in edges and edges[a][1]==edges[b][0] and (a,b) not in banned,'invalid or duplicate turn');banned.add((a,b))
    for n in out:out[n].sort()
    def solve(restricted):
        # State is incoming edge, not just node: reaching a node cheaply can forbid its next edge.
        dist={None:0};parent={};queue=[(0,'',None)];settled=set()
        while queue:
            cost,_,prev=heapq.heappop(queue)
            if prev in settled:continue
            settled.add(prev);node=start if prev is None else edges[prev][1]
            if node==end:
                path=[];k=prev
                while k is not None:path.append(k);k=parent[k]
                path.reverse();return {'cost':cost,'edges':path,'nodes':[start]+[edges[k][1] for k in path],'settled_states':len(settled)}
            for k in out[node]:
                if restricted and (prev,k) in banned:continue
                nxt=cost+edges[k][2]
                if k not in dist or nxt<dist[k]:dist[k]=nxt;parent[k]=prev;heapq.heappush(queue,(nxt,k,k))
        return None
    route=solve(True);baseline=solve(False)
    return {'route':route,'without_restrictions':baseline,'extra_cost':None if route is None or baseline is None else route['cost']-baseline['cost'],'exit_code':int(route is None)}

if __name__ == '__main__':
    raise SystemExit(main())
