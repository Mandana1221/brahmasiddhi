import re
from collections import Counter
t=open('/home/user/brahmasiddhi/NBh_text.txt').read()
ss=re.findall(r'(?m)^nys_(\d+),(\d+)\.(\d+):',t)
exp={('1','1'):41,('1','2'):20,('2','1'):68,('2','2'):69,('3','1'):72,('3','2'):72,('4','1'):68,('4','2'):51,('5','1'):43,('5','2'):24}
print(len(ss))
for k,n in exp.items():
    have=[int(x) for a,b,x in ss if (a,b)==k]
    miss=[i for i in range(1,n+1) if i not in have]; extra=[x for x in have if x>n]
    dup=[x for x,v in Counter(have).items() if v>1]
    print(k,'miss',miss,'extra',extra,'dup',dup)
print('other',[s for s in ss if (s[0],s[1]) not in exp])
# order check
seq=[(int(a),int(b),int(c)) for a,b,c in ss]
print('order breaks',[(seq[i-1],seq[i]) for i in range(1,len(seq)) if seq[i]<seq[i-1]][:20])
