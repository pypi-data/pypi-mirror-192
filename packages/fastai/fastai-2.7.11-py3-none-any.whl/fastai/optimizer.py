# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/12_optimizer.ipynb.

# %% ../nbs/12_optimizer.ipynb 2
from __future__ import annotations
from .torch_basics import *

# %% auto 0
__all__ = ['pytorch_hp_map', 'Optimizer', 'sgd_step', 'weight_decay', 'l2_reg', 'average_grad', 'average_sqr_grad',
           'momentum_step', 'SGD', 'rms_prop_step', 'RMSProp', 'step_stat', 'debias', 'adam_step', 'Adam', 'radam_step',
           'RAdam', 'qhadam_step', 'QHAdam', 'larc_layer_lr', 'larc_step', 'Larc', 'lamb_step', 'Lamb', 'Lookahead',
           'ranger', 'detuplify_pg', 'set_item_pg', 'OptimWrapper']

# %% ../nbs/12_optimizer.ipynb 6
class _BaseOptimizer():
    "Common functionality between `Optimizer` and `OptimWrapper`"
    def all_params(self,
        n:slice|int=slice(None), # Extended slicing over the optimizer `param_lists`
        with_grad:bool=False # Get all param tuples. If `True` select only those with a gradient
    ):
        res = L((p,pg,self.state[p],hyper) for pg,hyper in zip(self.param_lists[n],self.hypers[n]) for p in pg)
        return L(o for o in res if hasattr(o[0], 'grad') and o[0].grad is not None) if with_grad else res

    def _set_require_grad(self,
        rg:bool, # Requires grad: if `True` sets gradient for parameters, else uses state `state["force_train"]`
        p:Tensor, # Parameters to set gradient
        pg, # Param groups (unused but needed because unpack *o)
        state: dict,
        h # Hyperparameter (unused but needed because unpack *o)
    ):
        p.requires_grad_(rg or state.get('force_train', False))
    def freeze_to(self,
        n:int # Freeze up to `n` layers
    ):
        self.frozen_idx = n if n >= 0 else len(self.param_lists) + n
        if self.frozen_idx >= len(self.param_lists):
            warn(f"Freezing {self.frozen_idx} groups; model has {len(self.param_lists)}; whole model is frozen.")
        for o in self.all_params(slice(n, None)): self._set_require_grad(True,  *o)
        for o in self.all_params(slice(None, n)): self._set_require_grad(False, *o)

    def freeze(self):
        assert(len(self.param_lists)>1)
        self.freeze_to(-1)

    def set_hypers(self, **kwargs): L(kwargs.items()).starmap(self.set_hyper)
    def _set_hyper(self,
        k, # Hyperparameter key
        v # Hyperparameter value
    ):
        for v_,h in zip(v, self.hypers): h[k] = v_
    def set_hyper(self,
        k, # Hyperparameter key or slice of keys
        v # Hyperparameter value or slice of values
    ):
        if isinstance(v, slice):
            if v.start: v = even_mults(v.start, v.stop, len(self.param_lists))
            else: v = [v.stop/10]*(len(self.param_lists)-1) + [v.stop]
        v = L(v, use_list=None)
        if len(v)==1: v = v*len(self.param_lists)
        assert len(v) == len(self.hypers), f"Trying to set {len(v)} values for {k} but there are {len(self.param_lists)} parameter groups."
        self._set_hyper(k, v)

    def unfreeze(self): self.freeze_to(0)
    @property
    def param_groups(self): return [{**{'params': pg}, **hp} for pg,hp in zip(self.param_lists, self.hypers)]
    @param_groups.setter
    def param_groups(self,
        v:dict # List of dicts to set `params` and other hyper parameters
    ):
        for pg,v_ in zip(self.param_lists,v): pg = v_['params']
        for hyper,v_ in zip(self.hypers,v):
            for k,t in v_.items():
                if k != 'params': hyper[k] = t

# %% ../nbs/12_optimizer.ipynb 8
def _update(
    state:dict,
    new=None # New values to update `state` dict
):
    if new is None: return state
    if isinstance(new, dict): state.update(new)
    return state

# %% ../nbs/12_optimizer.ipynb 10
class Optimizer(_BaseOptimizer):
    "Base optimizer class for the fastai library, updating `params` with `cbs`"
    _keep_on_clear = ['force_train', 'do_wd']
    def __init__(self,
        params:Tensor|Iterable, # Model parameters
        cbs:callable|MutableSequence, # `Optimizer` step callbacks
        **defaults # Hyper parameters default values
    ):
        if 'train_bn' in defaults.keys():
            _ = defaults.pop('train_bn') 
            warn('Setting `train_bn` in `Optimizer` has no effect. Set `train_bn` on `Learner` init instead')
        params = L(params)
        self.cbs,self.state = L(cbs),defaultdict(dict)
        defaults = merge(*self.cbs.attrgot('defaults'), defaults)
        self.param_lists = L(L(p) for p in params) if isinstance(params[0], (L,list)) else L([params])
        self.hypers = L({} for _ in range_of(self.param_lists))
        self.set_hypers(**defaults)
        self.frozen_idx = 0

    def zero_grad(self):
        for p,*_ in self.all_params(with_grad=True):
            p.grad.detach_()
            p.grad.zero_()

    def step(self, closure=None):
        if closure is not None: raise NotImplementedError("fastai optimizers currently do not support closure")
        for p,pg,state,hyper in self.all_params(with_grad=True):
            for cb in self.cbs: state = _update(state, cb(p, **{**state, **hyper}))
            self.state[p] = state

    def clear_state(self):
        for p,pg,state,hyper in self.all_params():
            self.state[p] = {k: state[k] for k in self._keep_on_clear if k in state}

    def state_dict(self):
        state = [self.state[p] for p,*_ in self.all_params()]
        return {'state': state, 'hypers': self.hypers}

    def load_state_dict(self,
        sd:dict # State dict with `hypers` and `state` to load on the optimizer
    ):
        assert len(sd["hypers"]) == len(self.param_lists)
        assert len(sd["state"])  == sum([len(pg) for pg in self.param_lists])
        self.hypers = sd['hypers']
        self.state = {p: s for p,s in zip(self.all_params().itemgot(0), sd['state'])}

# %% ../nbs/12_optimizer.ipynb 21
def sgd_step(p, lr, **kwargs):
    p.data.add_(p.grad.data, alpha=-lr)

# %% ../nbs/12_optimizer.ipynb 24
def weight_decay(p, lr, wd, do_wd=True, **kwargs):
    "Weight decay as decaying `p` with `lr*wd`"
    if do_wd and wd!=0: p.data.mul_(1 - lr*wd)

weight_decay.defaults = dict(wd=0.)

# %% ../nbs/12_optimizer.ipynb 26
def l2_reg(p, lr, wd, do_wd=True, **kwargs):
    "L2 regularization as adding `wd*p` to `p.grad`"
    if do_wd and wd!=0: p.grad.data.add_(p.data, alpha=wd)

l2_reg.defaults = dict(wd=0.)

# %% ../nbs/12_optimizer.ipynb 41
def average_grad(p, mom, dampening=False, grad_avg=None, **kwargs):
    "Keeps track of the avg grads of `p` in `state` with `mom`."
    if grad_avg is None: grad_avg = torch.zeros_like(p.grad.data)
    damp = 1-mom if dampening else 1.
    grad_avg.mul_(mom).add_(p.grad.data, alpha=damp)
    return {'grad_avg': grad_avg}

average_grad.defaults = dict(mom=0.9)

# %% ../nbs/12_optimizer.ipynb 44
def average_sqr_grad(p, sqr_mom, dampening=True, sqr_avg=None, **kwargs):
    if sqr_avg is None: sqr_avg = torch.zeros_like(p.grad.data)
    damp = 1-sqr_mom if dampening else 1.
    sqr_avg.mul_(sqr_mom).addcmul_(p.grad.data, p.grad.data, value=damp)
    return {'sqr_avg': sqr_avg}

average_sqr_grad.defaults = dict(sqr_mom=0.99)

# %% ../nbs/12_optimizer.ipynb 62
def momentum_step(p, lr, grad_avg, **kwargs):
    "Step for SGD with momentum with `lr`"
    p.data.add_(grad_avg, alpha=-lr)

# %% ../nbs/12_optimizer.ipynb 63
def SGD(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0., # Gradient moving average (β1) coefficient
    wd:Real=0., # Optional weight decay (true or L2)
    decouple_wd:bool=True # Apply true weight decay or L2 regularization (SGD)
) -> Optimizer:
    "A SGD `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    if mom != 0: cbs.append(average_grad)
    cbs.append(sgd_step if mom==0 else momentum_step)
    return Optimizer(params, cbs, lr=lr, mom=mom, wd=wd)

# %% ../nbs/12_optimizer.ipynb 70
def rms_prop_step(p, lr, sqr_avg, eps, grad_avg=None, **kwargs):
    "Step for RMSProp with momentum with `lr`"
    denom = sqr_avg.sqrt().add_(eps)
    p.data.addcdiv_((grad_avg if grad_avg is not None else p.grad), denom, value=-lr)

rms_prop_step.defaults = dict(eps=1e-8)

# %% ../nbs/12_optimizer.ipynb 71
def RMSProp(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0., # Gradient moving average (β1) coefficient
    sqr_mom:float=0.99, # Gradient squared moving average (β2) coefficient
    eps:float=1e-8, # Added for numerical stability
    wd:Real=0., # Optional weight decay (true or L2)
    decouple_wd:bool=True # Apply true weight decay or L2 regularization (RMSProp)
) -> Optimizer:
    "A RMSProp `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += ([average_sqr_grad] if mom==0. else [average_grad, average_sqr_grad])
    cbs.append(rms_prop_step)
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, wd=wd)

# %% ../nbs/12_optimizer.ipynb 76
def step_stat(p, step=0, **kwargs):
    "Register the number of steps done in `state` for `p`"
    step += 1
    return {'step' : step}

# %% ../nbs/12_optimizer.ipynb 78
def debias(mom, damp, step): return damp * (1 - mom**step) / (1-mom)

# %% ../nbs/12_optimizer.ipynb 79
def adam_step(p, lr, mom, step, sqr_mom, grad_avg, sqr_avg, eps, **kwargs):
    "Step for Adam with `lr` on `p`"
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    p.data.addcdiv_(grad_avg, (sqr_avg/debias2).sqrt() + eps, value = -lr / debias1)
    return p

adam_step._defaults = dict(eps=1e-5)

# %% ../nbs/12_optimizer.ipynb 80
def Adam(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0.9, # Gradient moving average (β1) coefficient
    sqr_mom:float=0.99, # Gradient squared moving average (β2) coefficient
    eps:float=1e-5, # Added for numerical stability
    wd:Real=0.01, # Optional weight decay (true or L2)
    decouple_wd:bool=True # Apply true weight decay (AdamW) or L2 regularization (Adam)
) -> Optimizer:
    "A Adam/AdamW `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), average_sqr_grad, step_stat, adam_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd)

# %% ../nbs/12_optimizer.ipynb 85
def radam_step(p, lr, mom, step, sqr_mom, grad_avg, sqr_avg, eps, beta, **kwargs):
    "Step for RAdam with `lr` on `p`"
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    r_inf = 2/(1-sqr_mom) - 1
    r = r_inf - 2*step*sqr_mom**step/(1-sqr_mom**step)
    if r > 5:
        v = math.sqrt(((r-4) * (r-2) * r_inf)/((r_inf-4)*(r_inf-2)*r))
        denom = (sqr_avg/debias2).sqrt()
        if eps: denom += eps
        if beta: denom = F.softplus(denom, beta)
        p.data.addcdiv_(grad_avg, denom, value = -lr*v / debias1)
    else: p.data.add_(grad_avg, alpha=-lr / debias1)
    return p

radam_step._defaults = dict(eps=1e-5)

# %% ../nbs/12_optimizer.ipynb 86
def RAdam(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0.9, # Gradient moving average (β1) coefficient
    sqr_mom:float=0.99, # Gradient squared moving average (β2) coefficient
    eps:float=1e-5, # Added for numerical stability
    wd:Real=0., # Optional weight decay (true or L2)
    beta:float=0., # Set to enable SAdam
    decouple_wd:bool=True # Apply true weight decay (RAdamW) or L2 regularization (RAdam)
) -> Optimizer:
    "A RAdam/RAdamW `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), average_sqr_grad, step_stat, radam_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd, beta=beta)

# %% ../nbs/12_optimizer.ipynb 92
def qhadam_step(p, lr, mom, sqr_mom, sqr_avg, nu_1, nu_2, step, grad_avg, eps, **kwargs):
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    p.data.addcdiv_(((1-nu_1) * p.grad.data) + (nu_1 * (grad_avg / debias1)),
                    (((1 - nu_2) * (p.grad.data)**2) + (nu_2 * (sqr_avg / debias2))).sqrt() + eps,
                    value = -lr)
    return p

qhadam_step._defaults = dict(eps=1e-8)

# %% ../nbs/12_optimizer.ipynb 93
def QHAdam(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0.999, # Gradient moving average (β1) coefficient
    sqr_mom:float=0.999, # Gradient squared moving average (β2) coefficient
    nu_1:float=0.7, # QH immediate discount factor
    nu_2:float=1.0, # QH momentum discount factor
    eps:float=1e-8, # Added for numerical stability
    wd:Real=0., # Optional weight decay (true or L2)
    decouple_wd:bool=True, # Apply true weight decay (QHAdamW) or L2 regularization (QHAdam)
) -> Optimizer:
    "A QHAdam/QHAdamW `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), partial(average_sqr_grad, dampening=True), step_stat, qhadam_step]
    return Optimizer(params, cbs, lr=lr, nu_1=nu_1, nu_2=nu_2 ,
                     mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd)

# %% ../nbs/12_optimizer.ipynb 96
def larc_layer_lr(p, lr, trust_coeff, wd, eps, clip=True, **kwargs):
    "Computes the local lr before weight decay is applied"
    p_norm,g_norm = torch.norm(p.data),torch.norm(p.grad.data)
    local_lr = lr*trust_coeff * (p_norm) / (g_norm + p_norm * wd + eps)
    return {'local_lr': min(lr, local_lr) if clip else local_lr}

larc_layer_lr.defaults = dict(trust_coeff=0.02, wd=0., eps=1e-8)

# %% ../nbs/12_optimizer.ipynb 97
def larc_step(p, local_lr, grad_avg=None, **kwargs):
    "Step for LARC `local_lr` on `p`"
    p.data.add_(p.grad.data if grad_avg is None else grad_avg, alpha = -local_lr)

# %% ../nbs/12_optimizer.ipynb 98
def Larc(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0.9, # Gradient moving average (β1) coefficient
    clip:bool=True, # LARC if clip=True, LARS if clip=False
    trust_coeff:float=0.02, # Trust coeffiecnet for calculating layerwise LR
    eps:float=1e-8, # Added for numerical stability
    wd:Real=0., # Optional weight decay (true or L2)
    decouple_wd:bool=True # Apply true weight decay or L2 regularization
) -> Optimizer:
    "A LARC/LARS `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    if mom!=0.: cbs.append(average_grad)
    cbs += [partial(larc_layer_lr, clip=clip), larc_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, trust_coeff=trust_coeff, eps=eps, wd=wd)

# %% ../nbs/12_optimizer.ipynb 103
def lamb_step(p, lr, mom, step, sqr_mom, grad_avg, sqr_avg, eps, **kwargs):
    "Step for LAMB with `lr` on `p`"
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    r1 = p.data.pow(2).mean().sqrt()
    step = (grad_avg/debias1) / ((sqr_avg/debias2).sqrt()+eps)
    r2 = step.pow(2).mean().sqrt()
    q = 1 if r1 == 0 or r2 == 0 else min(r1/r2,10)
    p.data.add_(step, alpha = -lr * q)

lamb_step._defaults = dict(eps=1e-6, wd=0.)

# %% ../nbs/12_optimizer.ipynb 104
def Lamb(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0.9, # Gradient moving average (β1) coefficient
    sqr_mom:float=0.99, # Gradient squared moving average (β2) coefficient
    eps:float=1e-5, # Added for numerical stability
    wd:Real=0., # Optional weight decay (true or L2)
    decouple_wd:bool=True # Apply true weight decay or L2 regularization
) -> Optimizer:
    "A LAMB `Optimizer`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), average_sqr_grad, step_stat, lamb_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd)

# %% ../nbs/12_optimizer.ipynb 109
class Lookahead(Optimizer, GetAttr):
    "Wrap `opt` in a lookahead optimizer"
    _default='opt'
    def __init__(self, 
        opt:Optimizer, # `Optimizer` to wrap with Lookahead
        k:int=6, # How often to conduct Lookahead step
        alpha:float=0.5, # Slow weight moving average coefficient
    ):
        store_attr('opt,k,alpha')
        self._init_state()

    def step(self, closure=None):
        if closure is not None: raise NotImplementedError("fastai optimizers currently do not support closure")
        if self.slow_weights is None: self._copy_weights()
        self.opt.step()
        self.count += 1
        if self.count%self.k != 0: return
        for slow_pg,fast_pg in zip(self.slow_weights,self.param_lists):
            for slow_p,fast_p in zip(slow_pg,fast_pg):
                slow_p.data.add_(fast_p.data-slow_p.data, alpha=self.alpha)
                fast_p.data.copy_(slow_p.data)

    def clear_state(self):
        self.opt.clear_state()
        self._init_state()

    def state_dict(self):
        state = self.opt.state_dict()
        state.update({'count': self.count, 'slow_weights': self.slow_weights})
        return state

    def load_state_dict(self, sd):
        self.count = sd.pop('count')
        self.slow_weights = sd.pop('slow_weights')
        self.opt.load_state_dict(sd)

    def _init_state(self): self.count,self.slow_weights = 0,None
    def _copy_weights(self): self.slow_weights = L(L(p.clone().detach() for p in pg) for pg in self.param_lists)

    @property
    def param_lists(self): return self.opt.param_lists
    @param_lists.setter
    def param_lists(self, v): self.opt.param_lists = v

# %% ../nbs/12_optimizer.ipynb 111
@delegates(RAdam)
def ranger(
    params:Tensor|Iterable, # Model parameters
    lr:float|slice, # Default learning rate
    mom:float=0.95, # Gradient moving average (β1) coefficient
    wd:Real=0.01, # Optional weight decay (true or L2)
    eps:float=1e-6, # Added for numerical stability
    k:int=6, # How often to conduct Lookahead step
    alpha:float=0.5, # Slow weight moving average coefficient 
    **kwargs
) -> Lookahead:
    "Convenience method for `Lookahead` with `RAdam`"
    return Lookahead(RAdam(params, lr=lr, mom=mom, wd=wd, eps=eps, **kwargs), k=k, alpha=alpha)

# %% ../nbs/12_optimizer.ipynb 114
def detuplify_pg(d):
    res = {}
    for k,v in d.items():
        if k == 'params': continue
        if is_listy(v): res.update(**{f'{k}__{i}': v_ for i,v_ in enumerate(v)})
        else: res[k] = v
    return res

# %% ../nbs/12_optimizer.ipynb 116
def set_item_pg(pg, k, v):
    if '__' not in k: pg[k] = v
    else:
        name,idx = k.split('__')
        pg[name] = tuple(v if i==int(idx) else pg[name][i] for i in range_of(pg[name]))
    return pg

# %% ../nbs/12_optimizer.ipynb 118
pytorch_hp_map = {'momentum': 'mom', 'weight_decay': 'wd', 'alpha': 'sqr_mom', 'betas__0': 'mom',
                  'betas__1': 'sqr_mom'}

# %% ../nbs/12_optimizer.ipynb 119
def _convert_params(o:list) -> list:
    splitter = []
    for group in o:
        if isinstance(group, dict): splitter.append(group)
        else: splitter.append({'params':group})
    return splitter

# %% ../nbs/12_optimizer.ipynb 120
class OptimWrapper(_BaseOptimizer, GetAttr):
    "A wrapper class for existing PyTorch optimizers"
    _xtra=['zero_grad', 'step', 'state_dict', 'load_state_dict']
    _default='opt'
    def __init__(self, 
         params:Tensor|Iterable=None, # Model parameters. Don't set if using a built optimizer
         opt:callable|torch.optim.Optimizer=None, # A torch optimizer constructor, or an already built optimizer 
         hp_map:dict=None, # A dictionary converting PyTorch optimizer keys to fastai's `Optimizer` keys. Defaults to `pytorch_hp_map`
         convert_groups:bool=True, # Convert parameter groups from splitter or pass unaltered to `opt`
         **kwargs
    ):
        if params is None and opt is None: raise ValueError("Both `params` and `opt` cannot be None.")
        if callable(opt):
            if convert_groups:
                params = L(params)
                convert_groups = isinstance(params[0], (L,list))
            self.opt = opt(_convert_params(params), **kwargs) if convert_groups else opt(params, **kwargs)
        else:
            if params is not None: raise ValueError("Tried using both `params` and a built optimizer. Just pass in `opt`.")
            self.opt = opt
        if hp_map is None: hp_map = pytorch_hp_map
        self.fwd_map = {k: hp_map[k] if k in hp_map else k for k in detuplify_pg(self.opt.param_groups[0]).keys()}
        self.bwd_map = {v:k for k,v in self.fwd_map.items()}
        self.state = defaultdict(dict, {})
        self.frozen_idx = 0

    @property
    def hypers(self):
        return [{self.fwd_map.get(k, k):v for k,v in detuplify_pg(pg).items() if k != 'params'} for pg in self.opt.param_groups]

    def _set_hyper(self, k, v):
        for pg,v_ in zip(self.opt.param_groups,v): pg = set_item_pg(pg, self.bwd_map[k], v_)

    def clear_state(self): self.opt.state = defaultdict(dict, {})

    @property
    def param_lists(self): return [pg['params'] for pg in self.opt.param_groups]
    @param_lists.setter
    def param_lists(self, v):
        for pg,v_ in zip(self.opt.param_groups,v): pg['params'] = v_
