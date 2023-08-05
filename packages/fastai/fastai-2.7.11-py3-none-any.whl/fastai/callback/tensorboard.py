# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/70a_callback.tensorboard.ipynb.

# %% ../../nbs/70a_callback.tensorboard.ipynb 3
from __future__ import annotations
from ..basics import *

# %% auto 0
__all__ = ['TensorBoardBaseCallback', 'TensorBoardCallback', 'TensorBoardProjectorCallback', 'projector_word_embeddings',
           'tensorboard_log']

# %% ../../nbs/70a_callback.tensorboard.ipynb 18
import tensorboard
from torch.utils.tensorboard import SummaryWriter
from .fp16 import ModelToHalf
from .hook import hook_output

# %% ../../nbs/70a_callback.tensorboard.ipynb 19
class TensorBoardBaseCallback(Callback):
    order = Recorder.order+1
    "Base class for tensorboard callbacks"
    def __init__(self): self.run_projector = False
        
    def after_pred(self):
        if self.run_projector: self.feat = _add_projector_features(self.learn, self.h, self.feat)
    
    def after_validate(self):
        if not self.run_projector: return
        self.run_projector = False
        self._remove()
        _write_projector_embedding(self.learn, self.writer, self.feat)
            
    def after_fit(self): 
        if self.run: self.writer.close()
        
    def _setup_projector(self):
        self.run_projector = True
        self.h = hook_output(self.learn.model[1][1] if not self.layer else self.layer)
        self.feat = {}
        
    def _setup_writer(self): self.writer = SummaryWriter(log_dir=self.log_dir)
    def __del__(self): self._remove()
    def _remove(self):
        if getattr(self, 'h', None): self.h.remove()

# %% ../../nbs/70a_callback.tensorboard.ipynb 21
class TensorBoardCallback(TensorBoardBaseCallback):
    "Saves model topology, losses & metrics for tensorboard and tensorboard projector during training"
    def __init__(self, log_dir=None, trace_model=True, log_preds=True, n_preds=9, projector=False, layer=None):
        super().__init__()
        store_attr()

    def before_fit(self):
        self.run = not hasattr(self.learn, 'lr_finder') and not hasattr(self, "gather_preds") and rank_distrib()==0
        if not self.run: return
        self._setup_writer()
        if self.trace_model:
            if hasattr(self.learn, 'mixed_precision'):
                raise Exception("Can't trace model in mixed precision, pass `trace_model=False` or don't use FP16.")
            b = self.dls.one_batch()
            self.learn._split(b)
            self.writer.add_graph(self.model, *self.xb)

    def after_batch(self):
        self.writer.add_scalar('train_loss', self.smooth_loss, self.train_iter)
        for i,h in enumerate(self.opt.hypers):
            for k,v in h.items(): self.writer.add_scalar(f'{k}_{i}', v, self.train_iter)

    def after_epoch(self):
        for n,v in zip(self.recorder.metric_names[2:-1], self.recorder.log[2:-1]):
            self.writer.add_scalar(n, v, self.train_iter)
        if self.log_preds:
            b = self.dls.valid.one_batch()
            self.learn.one_batch(0, b)
            preds = getcallable(self.loss_func, 'activation')(self.pred)
            out = getcallable(self.loss_func, 'decodes')(preds)
            x,y,its,outs = self.dls.valid.show_results(b, out, show=False, max_n=self.n_preds)
            tensorboard_log(x, y, its, outs, self.writer, self.train_iter)
            
    def before_validate(self):
        if self.projector: self._setup_projector()

# %% ../../nbs/70a_callback.tensorboard.ipynb 23
class TensorBoardProjectorCallback(TensorBoardBaseCallback):
    "Extracts and exports image featuers for tensorboard projector during inference"
    def __init__(self, log_dir=None, layer=None):
        super().__init__()
        store_attr()
    
    def before_fit(self):
        self.run = not hasattr(self.learn, 'lr_finder') and hasattr(self, "gather_preds") and rank_distrib()==0
        if not self.run: return
        self._setup_writer()

    def before_validate(self):
        self._setup_projector()

# %% ../../nbs/70a_callback.tensorboard.ipynb 25
def _write_projector_embedding(learn, writer, feat):
    lbls = [learn.dl.vocab[l] for l in feat['lbl']] if getattr(learn.dl, 'vocab', None) else None     
    vecs = feat['vec'].squeeze()
    writer.add_embedding(vecs, metadata=lbls, label_img=feat['img'], global_step=learn.train_iter)

# %% ../../nbs/70a_callback.tensorboard.ipynb 26
def _add_projector_features(learn, hook, feat):
    img = _normalize_for_projector(learn.x)
    first_epoch = True if learn.iter == 0 else False
    feat['vec'] = hook.stored if first_epoch else torch.cat((feat['vec'], hook.stored),0)
    feat['img'] = img           if first_epoch else torch.cat((feat['img'], img),0)
    if getattr(learn.dl, 'vocab', None):
        feat['lbl'] = learn.y if first_epoch else torch.cat((feat['lbl'], learn.y),0)
    return feat

# %% ../../nbs/70a_callback.tensorboard.ipynb 27
def _get_embeddings(model, layer):
    layer = model[0].encoder if layer == None else layer
    return layer.weight

# %% ../../nbs/70a_callback.tensorboard.ipynb 28
@typedispatch
def _normalize_for_projector(x:TensorImage):
    # normalize tensor to be between 0-1
    img = x.clone()
    sz = img.shape
    img = img.view(x.size(0), -1)
    img -= img.min(1, keepdim=True)[0]
    img /= img.max(1, keepdim=True)[0]
    img = img.view(*sz)
    return img

# %% ../../nbs/70a_callback.tensorboard.ipynb 29
from ..text.all import LMLearner, TextLearner

# %% ../../nbs/70a_callback.tensorboard.ipynb 30
def projector_word_embeddings(learn=None, layer=None, vocab=None, limit=-1, start=0, log_dir=None):
    "Extracts and exports word embeddings from language models embedding layers"
    if not layer:
        if   isinstance(learn, LMLearner):   layer = learn.model[0].encoder
        elif isinstance(learn, TextLearner): layer = learn.model[0].module.encoder
    emb = layer.weight
    img = torch.full((len(emb),3,8,8), 0.7)
    vocab = learn.dls.vocab[0] if vocab == None else vocab
    vocab = list(map(lambda x: f'{x}_', vocab))
    writer = SummaryWriter(log_dir=log_dir)
    end = start + limit if limit >= 0 else -1
    writer.add_embedding(emb[start:end], metadata=vocab[start:end], label_img=img[start:end])
    writer.close()

# %% ../../nbs/70a_callback.tensorboard.ipynb 32
from ..vision.data import *

# %% ../../nbs/70a_callback.tensorboard.ipynb 33
@typedispatch
def tensorboard_log(x:TensorImage, y: TensorCategory, samples, outs, writer, step):
    fig,axs = get_grid(len(samples), return_fig=True)
    for i in range(2):
        axs = [b.show(ctx=c) for b,c in zip(samples.itemgot(i),axs)]
    axs = [r.show(ctx=c, color='green' if b==r else 'red')
            for b,r,c in zip(samples.itemgot(1),outs.itemgot(0),axs)]
    writer.add_figure('Sample results', fig, step)

# %% ../../nbs/70a_callback.tensorboard.ipynb 34
from ..vision.core import TensorPoint,TensorBBox

# %% ../../nbs/70a_callback.tensorboard.ipynb 35
@typedispatch
def tensorboard_log(x:TensorImage, y: TensorImageBase|TensorPoint|TensorBBox, samples, outs, writer, step):
    fig,axs = get_grid(len(samples), return_fig=True, double=True)
    for i in range(2):
        axs[::2] = [b.show(ctx=c) for b,c in zip(samples.itemgot(i),axs[::2])]
    for x in [samples,outs]:
        axs[1::2] = [b.show(ctx=c) for b,c in zip(x.itemgot(0),axs[1::2])]
    writer.add_figure('Sample results', fig, step)
