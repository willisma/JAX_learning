import jax
from jax import lax, random, numpy as jnp

# NN lib built on top of JAX developed
import flax
from flax.core import freeze, unfreeze
from flax import linen as nn
from flax.training import train_state

from torchvision.datasets import MNIST
from torch.utils.data import DataLoader

import functools
from typing import Any, Callable, Sequence, Optional

import numpy as np
# import matplotlib.pyplot as plt

seed = 0

def init_params(model):
    key1, key2 = jax.random.split(jax.random.PRNGKey(seed))

    ## init dummy input
    x = jax.random.normal(key1, (10,))

    ## init call; remember jax handles state externally
    y, params = model.init_with_output(key2, x)

    print(y)
    print((jax.tree_map(lambda x: x.shape, params)))

    ## Note 1: automatic shape inference
    ##         notice that from above we did not specify shape of input; the input shape is inferred
    ## Note 2: immutable structure (hence frozen dict)
    ## Note 3: init_with_output will produce the inference as another output
    return params

if __name__ == '__main__':
    ## single forward-feed layer
    model = nn.Dense(features=5)

    ## All Flax NN layer inherit from the Module class
    print(nn.Dense.__base__)

    params = init_params(model)
    key = jax.random.PRNGKey(seed)
    x = jax.random.normal(key, (10,))

    ## Will model correctly infer the shape here? Nope, params init with shape (10)
    y = model.apply(params, x)
    print(y)

    ## Also this does not work anymore
    try:
        y = model(x)
    except Exception as e:
        print(e) # --> unbound module

    ##### Simple Linear Reg

    n_samples = 1000
    x_dim = 2
    y_dim = 1
    noise_amp = 0.1

    ## Generate gt W & b
    key, w_k, b_k = jax.random.split(jax.random.PRNGKey(seed), num=3)
    W = jax.random.normal(w_k, (x_dim, y_dim))
    b = jax.random.normal(b_k, (y_dim,))

    true_params = freeze({'params': {'bias': b, 'kernel': W}})

    ## Generate Data
    key, x_k, eps_k = jax.random.split(key, num=3)
    xs = jax.random.normal(x_k, (n_samples, x_dim))
    ys = jnp.dot(xs, W) + b
    ys += noise_amp * jax.random.normal(eps_k, (n_samples, y_dim))

    print(f"input shape: {xs.shape}, target shape: {ys.shape}")
 


