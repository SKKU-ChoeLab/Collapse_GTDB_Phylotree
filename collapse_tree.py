##### version control #####

#dependencies:
#  - python=3.6.13
#  - ete3=3.1.3
#  source GTDB taxonomy=bac120_taxonomy_r226.tsv
#  default GTDB tree=bac120.sp_labels.tree

#######################

import re
from ete3 import Tree, TreeStyle

IN_FILE  = "bac120.sp_labels.tree"
OUT_FILE = "bac120.species_collapsed.tree"


num_prefix_re = re.compile(r"^\s*\d+(?:\.\d+)?:\s*(.+)$")
num_only_re   = re.compile(r"^\s*\d+(?:\.\d+)?\s*$")

def normalize_label(name: str) -> str:
    if not name:
        return ""
    s = str(name).strip("'\"")
    m = num_prefix_re.match(s)
    if m:
        s = m.group(1)
    if num_only_re.match(s):
        return ""
    return s

def needs_quotes(s: str) -> bool:
    return (" " in s) and (not (s.startswith("'") and s.endswith("'")))

def ensure_quoted(name: str) -> str:
    if not name:
        return ""
    s = name
    if needs_quotes(s):
        s = "'" + s.strip("'") + "'"
    return s

def rank_of(name: str):
    if not name or "__" not in name:
        return None
    rk, _ = name.split("__", 1)
    rk = rk.lower()
    return rk if rk in {"d","p","c","o","f","g","s"} else None


t = Tree(IN_FILE, format=1, quoted_node_names=True)

for n in t.traverse("postorder"):
    n.name = normalize_label(n.name)

for n in t.traverse("postorder"):
    if rank_of(n.name) == "g":
        n.children = []

for lf in list(t.iter_leaves()):
    if rank_of(lf.name) == "s":
        lf.detach()

for n in t.traverse("postorder"):
    if n.is_leaf():
        continue
    r = rank_of(n.name)
    if r in {"f","o","c","p","d"}:
        pass
    else:
        n.name = "" 

changed = True
while changed:
    changed = False
    for n in list(t.traverse("postorder")):
        if n.is_root() or n.is_leaf():
            continue
        if not n.name and len(n.children) == 1:
            n.delete(prevent_nondicotomic=False)
            changed = True

uid = 0
for node in t.traverse():
    name = node.name or ""
    if node.is_leaf() and not name:
        node.name = f"UNLABELED_{uid}"; uid += 1
    node.name = ensure_quoted(node.name)

t.write(format=1, outfile=OUT_FILE)
print(f"[OK] wrote: {OUT_FILE}")

