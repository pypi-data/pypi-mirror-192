# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/07_merge.ipynb.

# %% auto 0
__all__ = ['conf_re', 'unpatch', 'nbdev_fix', 'nbdev_merge']

# %% ../nbs/api/07_merge.ipynb 2
from .imports import *
from .config import *
from .export import *
from .sync import *

from execnb.nbio import *
from fastcore.script import *
from fastcore import shutil

import subprocess
from difflib import SequenceMatcher

# %% ../nbs/api/07_merge.ipynb 16
_BEG,_MID,_END = '<'*7,'='*7,'>'*7
conf_re = re.compile(rf'^{_BEG}\s+(\S+)\n(.*?)^{_MID}\n(.*?)^{_END}\s+([\S ]+)\n', re.MULTILINE|re.DOTALL)

def _unpatch_f(before, cb1, cb2, c, r):
    if cb1 is not None and cb1 != cb2: raise Exception(f'Branch mismatch: {cb1}/{cb2}')
    r.append(before)
    r.append(c)
    return cb2

# %% ../nbs/api/07_merge.ipynb 17
def unpatch(s:str):
    "Takes a string with conflict markers and returns the two original files, and their branch names"
    *main,last = conf_re.split(s)
    r1,r2,c1b,c2b = [],[],None,None
    for before,c1_branch,c1,c2,c2_branch in chunked(main, 5):
        c1b = _unpatch_f(before, c1b, c1_branch, c1, r1)
        c2b = _unpatch_f(before, c2b, c2_branch, c2, r2)
    return ''.join(r1+[last]), ''.join(r2+[last]), c1b, c2b

# %% ../nbs/api/07_merge.ipynb 22
def _make_md(code): return [dict(source=f'`{code}`', cell_type="markdown", metadata={})]
def _make_conflict(a,b, branch1, branch2):
    return _make_md(f'{_BEG} {branch1}') + a+_make_md(_MID)+b + _make_md(f'{_END} {branch2}')

def _merge_cells(a, b, brancha, branchb, theirs):
    matches = SequenceMatcher(None, a, b).get_matching_blocks()
    res,prev_sa,prev_sb,conflict = [],0,0,False
    for sa,sb,sz in matches:
        ca,cb = a[prev_sa:sa],b[prev_sb:sb]
        if ca or cb:
            res += _make_conflict(ca, cb, brancha, branchb)
            conflict = True
        if sz: res += b[sb:sb+sz] if theirs else a[sa:sa+sz]
        prev_sa,prev_sb = sa+sz,sb+sz
    return res,conflict

# %% ../nbs/api/07_merge.ipynb 23
@call_parse
def nbdev_fix(nbname:str, # Notebook filename to fix
               outname:str=None, # Filename of output notebook (defaults to `nbname`)
               nobackup:bool_arg=True, # Do not backup `nbname` to `nbname`.bak if `outname` not provided
               theirs:bool=False, # Use their outputs and metadata instead of ours
               noprint:bool=False): # Do not print info about whether conflicts are found
    "Create working notebook from conflicted notebook `nbname`"
    nbname = Path(nbname)
    if not nobackup and not outname: shutil.copy(nbname, nbname.with_suffix('.ipynb.bak'))
    nbtxt = nbname.read_text()
    a,b,branch1,branch2 = unpatch(nbtxt)
    ac,bc = dict2nb(loads(a)),dict2nb(loads(b))
    dest = bc if theirs else ac
    cells,conflict = _merge_cells(ac.cells, bc.cells, branch1, branch2, theirs=theirs)
    dest.cells = cells
    write_nb(dest, ifnone(outname, nbname))
    if not noprint:
        if conflict: print("One or more conflict remains in the notebook, please inspect manually.")
        else: print("Successfully merged conflicts!")
    return conflict

# %% ../nbs/api/07_merge.ipynb 27
def _git_branch_merge():
    try: return only(v for k,v in os.environ.items() if k.startswith('GITHEAD'))
    except ValueError: return

# %% ../nbs/api/07_merge.ipynb 28
def _git_rebase_head():
    for d in ('apply','merge'):
        d = Path(f'.git/rebase-{d}')
        if d.is_dir():
            cmt = (d/'orig-head').read_text()
            msg = run(f'git show-branch --no-name {cmt}')
            return f'{cmt[:7]} ({msg})'

# %% ../nbs/api/07_merge.ipynb 29
def _git_merge_file(base, ours, theirs):
    "`git merge-file` with expected labels depending on if a `merge` or `rebase` is in-progress"
    l_theirs = _git_rebase_head() or _git_branch_merge() or 'THEIRS'
    cmd = f"git merge-file -L HEAD -L BASE -L '{l_theirs}' {ours} {base} {theirs}"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

# %% ../nbs/api/07_merge.ipynb 30
@call_parse
def nbdev_merge(base:str, ours:str, theirs:str, path:str):
    "Git merge driver for notebooks"
    if not _git_merge_file(base, ours, theirs).returncode: return
    theirs = str2bool(os.environ.get('THEIRS', False))
    return nbdev_fix.__wrapped__(ours, theirs=theirs)
