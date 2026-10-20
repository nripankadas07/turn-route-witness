import copy,itertools,json,pathlib,random,sqlite3,subprocess,sys,tempfile,unittest
from turn_route_witness import analyze
ROOT=pathlib.Path(__file__).absolute().parent
def example():return json.loads((ROOT/'example.json').read_text())
class Contract(unittest.TestCase):
    def test_strict_cli_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)/'bad.json'
            for raw in ('{', '{"x":1,"x":2}', '{"x":NaN}', '{}', ' '*1048577):
                p.write_text(raw);r=subprocess.run([sys.executable,str(ROOT/'turn_route_witness.py'),str(p)],text=True,capture_output=True,timeout=5)
                self.assertEqual(r.returncode,2);self.assertTrue(r.stderr);self.assertFalse(r.stdout)
    def test_input_unchanged(self):
        x=example();saved=copy.deepcopy(x);analyze(x);self.assertEqual(x,saved)

    def test_incoming_state_required(self):
        r=analyze(example());self.assertEqual(r['route']['edges'],['ad','db','bc']);self.assertEqual(r['route']['cost'],4);self.assertEqual(r['extra_cost'],2)
    def test_unreachable_and_identity(self):
        d=example();d['edges']=[e for e in d['edges'] if e['id']!='ad'];r=analyze(d);self.assertIsNone(r['route']);self.assertEqual(r['exit_code'],1)
        d=example();d['end']='A';self.assertEqual(analyze(d)['route']['edges'],[])
    def test_parallel_zero_cycle(self):
        d=example();d['edges']+=[{'id':'loop','from':'B','to':'B','cost':0}];self.assertEqual(analyze(d)['route']['cost'],2)
    def test_invalid_turn_and_negative_cost(self):
        d=example();d['forbidden']=[['ab','db']]
        with self.assertRaises(ValueError):analyze(d)
        d=example();d['edges'][0]['cost']=-1
        with self.assertRaises(ValueError):analyze(d)
    def test_random_exhaustive_edge_state_paths(self):
        rng=random.Random(17)
        for _ in range(100):
            es=[{'id':str(i),'from':a,'to':b,'cost':rng.randrange(4)} for i,(a,b) in enumerate(itertools.permutations('ABC',2)) if rng.randrange(2)]
            turns=[[a['id'],b['id']] for a in es for b in es if a['to']==b['from'] and rng.randrange(3)==0]
            d={'nodes':list('ABC'),'edges':es,'forbidden':turns,'start':'A','end':'C'};costs=[]
            def walk(node,path,cost):
                if node=='C':costs.append(cost);return
                for e in es:
                    if e['from']==node and e['id'] not in path and (not path or [path[-1],e['id']] not in turns):walk(e['to'],path+[e['id']],cost+e['cost'])
            walk('A',[],0);out=analyze(d)['route'];self.assertEqual(None if out is None else out['cost'],min(costs) if costs else None)

if __name__ == '__main__':unittest.main()
