# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/14_callback.schedule.ipynb.

# %% ../../nbs/14_callback.schedule.ipynb 2
from __future__ import annotations
from ..basics import *
from .tracker import SaveModelCallback

# %% auto 0
__all__ = ['annealer', 'sched_lin', 'sched_cos', 'sched_no', 'sched_exp', 'SchedLin', 'SchedCos', 'SchedNo', 'SchedExp',
           'SchedPoly', 'combine_scheds', 'combined_cos', 'ParamScheduler', 'LRFinder', 'valley', 'slide', 'minimum',
           'steep', 'SuggestionMethod']

# %% ../../nbs/14_callback.schedule.ipynb 3
_all_ = ['SuggestionMethod']

# %% ../../nbs/14_callback.schedule.ipynb 8
class _Annealer:
    def __init__(self, f, start, end): store_attr('f,start,end')
    def __call__(self, pos): return self.f(self.start, self.end, pos)

# %% ../../nbs/14_callback.schedule.ipynb 9
def annealer(f):
    "Decorator to make `f` return itself partially applied."
    @functools.wraps(f)
    def _inner(start, end): return _Annealer(f, start, end)
    return _inner

# %% ../../nbs/14_callback.schedule.ipynb 11
#TODO Jeremy, make this pickle
#@annealer
#def SchedLin(start, end, pos): return start + pos*(end-start)
#@annealer
#def SchedCos(start, end, pos): return start + (1 + math.cos(math.pi*(1-pos))) * (end-start) / 2
#@annealer
#def SchedNo (start, end, pos): return start
#@annealer
#def SchedExp(start, end, pos): return start * (end/start) ** pos
#
#SchedLin.__doc__ = "Linear schedule function from `start` to `end`"
#SchedCos.__doc__ = "Cosine schedule function from `start` to `end`"
#SchedNo .__doc__ = "Constant schedule function with `start` value"
#SchedExp.__doc__ = "Exponential schedule function from `start` to `end`"

# %% ../../nbs/14_callback.schedule.ipynb 12
def sched_lin(start, end, pos): return start + pos*(end-start)
def sched_cos(start, end, pos): return start + (1 + math.cos(math.pi*(1-pos))) * (end-start) / 2
def sched_no (start, end, pos): return start
def sched_exp(start, end, pos): return start * (end/start) ** pos

def SchedLin(start, end): return _Annealer(sched_lin, start, end)
def SchedCos(start, end): return _Annealer(sched_cos, start, end)
def SchedNo (start, end): return _Annealer(sched_no,  start, end)
def SchedExp(start, end): return _Annealer(sched_exp, start, end)

SchedLin.__doc__ = "Linear schedule function from `start` to `end`"
SchedCos.__doc__ = "Cosine schedule function from `start` to `end`"
SchedNo .__doc__ = "Constant schedule function with `start` value"
SchedExp.__doc__ = "Exponential schedule function from `start` to `end`"

# %% ../../nbs/14_callback.schedule.ipynb 15
def SchedPoly(start, end, power):
    "Polynomial schedule (of `power`) function from `start` to `end`"
    def _inner(pos): return start + (end - start) * pos ** power
    return _inner

# %% ../../nbs/14_callback.schedule.ipynb 28
def combine_scheds(pcts, scheds):
    "Combine `scheds` according to `pcts` in one function"
    assert sum(pcts) == 1.
    pcts = tensor([0] + L(pcts))
    assert torch.all(pcts >= 0)
    pcts = torch.cumsum(pcts, 0)
    pct_lim = len(pcts) - 2
    def _inner(pos):
        idx = min((pos >= pcts).nonzero().max(), pct_lim)
        actual_pos = (pos-pcts[idx]) / (pcts[idx+1]-pcts[idx])
        return scheds[idx](actual_pos.item())
    return _inner

# %% ../../nbs/14_callback.schedule.ipynb 33
def combined_cos(pct, start, middle, end):
    "Return a scheduler with cosine annealing from `start`→`middle` & `middle`→`end`"
    return combine_scheds([pct,1-pct], [SchedCos(start, middle), SchedCos(middle, end)])

# %% ../../nbs/14_callback.schedule.ipynb 38
@docs
class ParamScheduler(Callback):
    "Schedule hyper-parameters according to `scheds`"
    order,run_valid = 60,False

    def __init__(self, scheds): self.scheds = scheds
    def before_fit(self): self.hps = {p:[] for p in self.scheds.keys()}
    def before_batch(self): self._update_val(self.pct_train)

    def _update_val(self, pct):
        for n,f in self.scheds.items(): self.opt.set_hyper(n, f(pct))

    def after_batch(self):
        for p in self.scheds.keys(): self.hps[p].append(self.opt.hypers[-1][p])

    def after_fit(self):
        if hasattr(self.learn, 'recorder') and hasattr(self, 'hps'): self.recorder.hps = self.hps

    _docs = {"before_fit": "Initialize container for hyper-parameters",
             "before_batch": "Set the proper hyper-parameters in the optimizer",
             "after_batch": "Record hyper-parameters of this batch",
             "after_fit": "Save the hyper-parameters in the recorder if there is one"}

# %% ../../nbs/14_callback.schedule.ipynb 46
@patch
def fit_one_cycle(self:Learner, n_epoch, lr_max=None, div=25., div_final=1e5, pct_start=0.25, wd=None,
                  moms=None, cbs=None, reset_opt=False, start_epoch=0):
    "Fit `self.model` for `n_epoch` using the 1cycle policy."
    if self.opt is None: self.create_opt()
    self.opt.set_hyper('lr', self.lr if lr_max is None else lr_max)
    lr_max = np.array([h['lr'] for h in self.opt.hypers])
    scheds = {'lr': combined_cos(pct_start, lr_max/div, lr_max, lr_max/div_final),
              'mom': combined_cos(pct_start, *(self.moms if moms is None else moms))}
    self.fit(n_epoch, cbs=ParamScheduler(scheds)+L(cbs), reset_opt=reset_opt, wd=wd, start_epoch=start_epoch)

# %% ../../nbs/14_callback.schedule.ipynb 50
@patch
def plot_sched(self:Recorder, keys=None, figsize=None):
    keys = self.hps.keys() if keys is None else L(keys)
    rows,cols = (len(keys)+1)//2, min(2, len(keys))
    figsize = figsize or (6*cols,4*rows)
    _, axs = plt.subplots(rows, cols, figsize=figsize)
    axs = axs.flatten() if len(keys) > 1 else L(axs)
    for p,ax in zip(keys, axs):
        ax.plot(self.hps[p])
        ax.set_ylabel(p)

# %% ../../nbs/14_callback.schedule.ipynb 54
@patch
def fit_flat_cos(self:Learner, n_epoch, lr=None, div_final=1e5, pct_start=0.75, wd=None,
                 cbs=None, reset_opt=False, start_epoch=0):
    "Fit `self.model` for `n_epoch` at flat `lr` before a cosine annealing."
    if self.opt is None: self.create_opt()
    self.opt.set_hyper('lr', self.lr if lr is None else lr)
    lr = np.array([h['lr'] for h in self.opt.hypers])
    scheds = {'lr': combined_cos(pct_start, lr, lr, lr/div_final)}
    self.fit(n_epoch, cbs=ParamScheduler(scheds)+L(cbs), reset_opt=reset_opt, wd=wd, start_epoch=0)

# %% ../../nbs/14_callback.schedule.ipynb 57
@patch
def fit_sgdr(self:Learner, n_cycles, cycle_len, lr_max=None, cycle_mult=2, cbs=None, reset_opt=False, wd=None,
             start_epoch=0):
    "Fit `self.model` for `n_cycles` of `cycle_len` using SGDR."
    if self.opt is None: self.create_opt()
    self.opt.set_hyper('lr', self.lr if lr_max is None else lr_max)
    lr_max = np.array([h['lr'] for h in self.opt.hypers])
    n_epoch = cycle_len * (cycle_mult**n_cycles-1)//(cycle_mult-1)
    pcts = [cycle_len * cycle_mult**i / n_epoch for i in range(n_cycles)]
    scheds = [SchedCos(lr_max, 0) for _ in range(n_cycles)]
    scheds = {'lr': combine_scheds(pcts, scheds)}
    self.fit(n_epoch, cbs=ParamScheduler(scheds)+L(cbs), reset_opt=reset_opt, wd=wd, start_epoch=start_epoch)

# %% ../../nbs/14_callback.schedule.ipynb 60
@patch
@delegates(Learner.fit_one_cycle)
def fine_tune(self:Learner, epochs, base_lr=2e-3, freeze_epochs=1, lr_mult=100,
              pct_start=0.3, div=5.0, **kwargs):
    "Fine tune with `Learner.freeze` for `freeze_epochs`, then with `Learner.unfreeze` for `epochs`, using discriminative LR."
    self.freeze()
    self.fit_one_cycle(freeze_epochs, slice(base_lr), pct_start=0.99, **kwargs)
    base_lr /= 2
    self.unfreeze()
    self.fit_one_cycle(epochs, slice(base_lr/lr_mult, base_lr), pct_start=pct_start, div=div, **kwargs)

# %% ../../nbs/14_callback.schedule.ipynb 67
@docs
class LRFinder(ParamScheduler):
    "Training with exponentially growing learning rate"
    def __init__(self, start_lr=1e-7, end_lr=10, num_it=100, stop_div=True):
        if num_it < 6: num_it = 6
        self.scheds = {'lr': [SchedExp(s, e) for (s,e) in zip(start_lr,end_lr)
                             ] if is_listy(start_lr) else SchedExp(start_lr, end_lr)}
        self.num_it,self.stop_div = num_it,stop_div

    def before_fit(self):
        super().before_fit()
        path = self.path/self.model_dir
        path.mkdir(parents=True, exist_ok=True)
        self.tmp_d = tempfile.TemporaryDirectory(dir=path)
        self.tmp_p = Path(self.tmp_d.name).stem
        self.learn.save(f'{self.tmp_p}/_tmp')
        self.best_loss = float('inf')

    def before_batch(self): self._update_val(self.train_iter/self.num_it)

    def after_batch(self):
        super().after_batch()
        if self.smooth_loss < self.best_loss: self.best_loss = self.smooth_loss
        if self.smooth_loss > 4*self.best_loss and self.stop_div: raise CancelFitException()
        if self.train_iter >= self.num_it: raise CancelFitException()

    def before_validate(self): raise CancelValidException()

    def after_fit(self):
        self.learn.opt.zero_grad() # Needed before detaching the optimizer for future fits
        tmp_f = self.path/self.model_dir/self.tmp_p/'_tmp.pth'
        if tmp_f.exists():
            self.learn.load(f'{self.tmp_p}/_tmp', with_opt=True)
            self.tmp_d.cleanup()

    _docs = {"before_fit": "Initialize container for hyper-parameters and save the model",
             "before_batch": "Set the proper hyper-parameters in the optimizer",
             "after_batch": "Record hyper-parameters of this batch and potentially stop training",
             "after_fit": "Save the hyper-parameters in the recorder if there is one and load the original model",
             "before_validate": "Skip the validation part of training"}

# %% ../../nbs/14_callback.schedule.ipynb 78
def valley(lrs:list, losses:list, num_it:int):
    "Suggests a learning rate from the longest valley and returns its index"
    n = len(losses)
    max_start, max_end = 0,0

    # find the longest valley
    lds = [1]*n
    for i in range(1,n):
        for j in range(0,i):
            if (losses[i] < losses[j]) and (lds[i] < lds[j] + 1):
                lds[i] = lds[j] + 1
            if lds[max_end] < lds[i]:
                max_end = i
                max_start = max_end - lds[max_end]
    
    sections = (max_end - max_start) / 3
    idx = max_start + int(sections) + int(sections/2)

    return float(lrs[idx]), (float(lrs[idx]), losses[idx])

# %% ../../nbs/14_callback.schedule.ipynb 81
def slide(lrs:list, losses:list, num_it:int, lr_diff:int=15, thresh:float=.005, adjust_value:float=1.):
    "Suggests a learning rate following an interval slide rule and returns its index"
    losses = to_np(losses)
    loss_grad = np.gradient(losses)

    r_idx = -1
    l_idx = r_idx - lr_diff
    local_min_lr = lrs[l_idx]
    while (l_idx >= -len(losses)) and (abs(loss_grad[r_idx] - loss_grad[l_idx]) > thresh):
        local_min_lr = lrs[l_idx]
        r_idx -= 1
        l_idx -= 1
    
    suggestion = float(local_min_lr) * adjust_value
    idx = np.interp(np.log10(suggestion), np.log10(lrs), losses)
    return suggestion, (suggestion, idx)

# %% ../../nbs/14_callback.schedule.ipynb 84
def minimum(lrs:list, losses:list, num_it:int):
    "Suggests a learning rate one-tenth the minumum before divergance and returns its index"
    lr_min = lrs[losses.argmin()].item()
    loss_idx = losses[min(range(len(lrs)), key=lambda i: abs(lrs[i]-lr_min))]
    return lr_min/10, (lr_min, loss_idx)

# %% ../../nbs/14_callback.schedule.ipynb 86
def steep(lrs:list, losses:list, num_it:int) -> (float, tuple):
    "Suggests a learning rate when the slope is the steepest and returns its index"
    grads = (losses[1:]-losses[:-1]) / (lrs[1:].log()-lrs[:-1].log())
    lr_steep = lrs[grads.argmin()].item()
    loss_idx = losses[min(range(len(lrs)), key=lambda i: abs(lrs[i]-lr_steep))]
    return lr_steep, (lr_steep, loss_idx)

# %% ../../nbs/14_callback.schedule.ipynb 88
@patch
def plot_lr_find(self:Recorder, skip_end=5, return_fig=True, suggestions=None, nms=None, **kwargs):
    "Plot the result of an LR Finder test (won't work if you didn't do `learn.lr_find()` before)"
    lrs    = self.lrs    if skip_end==0 else self.lrs   [:-skip_end]
    losses = self.losses if skip_end==0 else self.losses[:-skip_end]
    fig, ax = plt.subplots(1,1)
    ax.plot(lrs, losses)
    ax.set_ylabel("Loss")
    ax.set_xlabel("Learning Rate")
    ax.set_xscale('log')
    if suggestions:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][1:]
        for (val, idx), nm, color in zip(suggestions, nms, colors):
            ax.plot(val, idx, 'o', label=nm, c=color)
        ax.legend(loc='best')

# %% ../../nbs/14_callback.schedule.ipynb 89
mk_class("SuggestionMethod", **{o.__name__.capitalize():o for o in [valley,slide,minimum,steep]},
         doc="All possible suggestion methods as convience attributes to get tab-completion and typo-proofing")

# %% ../../nbs/14_callback.schedule.ipynb 90
@patch
def lr_find(self:Learner, start_lr=1e-7, end_lr=10, num_it=100, stop_div=True, show_plot=True, suggest_funcs=(SuggestionMethod.Valley)):
    "Launch a mock training to find a good learning rate and return suggestions based on `suggest_funcs` as a named tuple"
    n_epoch = num_it//len(self.dls.train) + 1
    cb=LRFinder(start_lr=start_lr, end_lr=end_lr, num_it=num_it, stop_div=stop_div)
    with self.no_logging(): self.fit(n_epoch, cbs=cb)
    if suggest_funcs is not None:
        lrs, losses = tensor(self.recorder.lrs[num_it//10:-5]), tensor(self.recorder.losses[num_it//10:-5])
        nan_idxs = torch.nonzero(torch.isnan(losses.view(-1)))
        if len(nan_idxs) > 0:
            drop_idx = min(nan_idxs)
            lrs = lrs[:drop_idx]
            losses = losses[:drop_idx]
        _suggestions, nms = [], []
        for func in tuplify(suggest_funcs):
            nms.append(func.__name__ if not isinstance(func, partial) else func.func.__name__) # deal with partials
            _suggestions.append(func(lrs, losses, num_it))
        
        SuggestedLRs = collections.namedtuple('SuggestedLRs', nms)
        lrs, pnts = [], []
        for lr, pnt in _suggestions:
            lrs.append(lr)
            pnts.append(pnt)
        if show_plot: self.recorder.plot_lr_find(suggestions=pnts, nms=nms)
        return SuggestedLRs(*lrs)

    elif show_plot: self.recorder.plot_lr_find()
