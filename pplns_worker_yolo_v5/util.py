
import os

def env(name : str) -> str:

  if name in os.environ:

    return os.environ[name]

  else: 

    raise Exception(f'Missng {name} in env.')