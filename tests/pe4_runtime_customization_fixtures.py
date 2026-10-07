"""Deterministic reviewed Linux observations; no production access."""
import copy
from pathlib import Path
PTH_BYTES=b"import os; var = 'SETUPTOOLS_USE_DISTUTILS'; enabled = os.environ.get(var, 'local') == 'local'; enabled and __import__('_distutils_hack').add_shim(); \n"
SITE_BYTES=b"# install the apport exception handler if available\ntry:\n    import apport_python_hook\nexcept ImportError:\n    pass\nelse:\n    apport_python_hook.install()\n"
def observation(site):
 return dict(pth_names=['distutils-precedence.pth'],pth=dict(path=str(site/'distutils-precedence.pth'),type='REGULAR',owner='jazofv1',group='jazofv1',mode=0o640,links=1,size=151,bytes=PTH_BYTES,sha256='2638ce9e2500e572a5e0de7faed6661eb569d1b696fcba07b0dd223da5f5d224'),setuptools_version='66.1.1',pth_records=[dict(path='distutils-precedence.pth',size=151,hash_mode='sha256',hash_value='JjjOniUA5XKl4N5_rtZmHrVp0baW_LoHsN0iPaX10iQ',located_path=str(site/'distutils-precedence.pth'))],site_loaded=True,site_module='/usr/lib/python3.11/sitecustomize.py',site_link=dict(path='/usr/lib/python3.11/sitecustomize.py',type='SYMLINK',owner='root',group='root',target='/etc/python3.11/sitecustomize.py',resolved='/etc/python3.11/sitecustomize.py'),site_target=dict(path='/etc/python3.11/sitecustomize.py',type='REGULAR',owner='root',group='root',mode=0o644,links=1,size=155,bytes=SITE_BYTES,sha256='43d81125d92376b1a69d53a71126a041cc9a18d8080e92dea0a2ae23be138b1e'),user_loaded=False,user_files=[])
def failures(site):
 good=observation(site)
 changes=[('pth_names',[]),('pth_names',['distutils-precedence.pth','other.pth']),('pth_names',['renamed.pth']),('setuptools_version',None),('setuptools_version','66.1.2'),('pth_records',[]),('site_loaded',False),('site_module','/other/sitecustomize.py'),('user_loaded',True),('user_files',['/other/usercustomize.py'])]
 for field,values in [('pth',dict(path='/other/distutils-precedence.pth',type='SYMLINK',owner='root',group='root',mode=0o644,links=2,size=150,bytes=PTH_BYTES[:-2]+b'X\n',sha256='0'*64)),('site_link',dict(path='/other/sitecustomize.py',type='REGULAR',owner='jazofv1',group='jazofv1',target='/other/sitecustomize.py',resolved='/other/sitecustomize.py')),('site_target',dict(path='/other/sitecustomize.py',type='SYMLINK',owner='jazofv1',group='jazofv1',mode=0o640,links=2,size=154,bytes=SITE_BYTES[:-1]+b'X',sha256='0'*64))]:
  for key,value in values.items():
   bad=copy.deepcopy(good);bad[field][key]=value;yield field+'.'+key,bad
 for key,value in dict(path='renamed.pth',size=150,hash_mode='md5',hash_value='wrong',located_path='/other/distutils-precedence.pth').items():
  bad=copy.deepcopy(good);bad['pth_records'][0][key]=value;yield 'record.'+key,bad
 for key,value in changes:
  bad=copy.deepcopy(good);bad[key]=value;yield key,bad
