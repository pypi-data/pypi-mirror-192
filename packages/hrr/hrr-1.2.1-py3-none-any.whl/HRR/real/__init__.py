try:
    from HRR.real.with_pytorch import *
except ImportError:
    pass

try:
    from HRR.real.with_jax import *
    from HRR.real.with_flax import *
except ImportError:
    pass

try:
    from HRR.real.with_tensorflow import *
except ImportError:
    pass
