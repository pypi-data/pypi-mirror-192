# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/41_tabular.data.ipynb.

# %% ../../nbs/41_tabular.data.ipynb 2
from __future__ import annotations
from ..torch_basics import *
from ..data.all import *
from .core import *

# %% auto 0
__all__ = ['TabularDataLoaders']

# %% ../../nbs/41_tabular.data.ipynb 7
class TabularDataLoaders(DataLoaders):
    "Basic wrapper around several `DataLoader`s with factory methods for tabular data"
    @classmethod
    @delegates(Tabular.dataloaders, but=["dl_type", "dl_kwargs"])
    def from_df(cls, 
        df:pd.DataFrame,
        path:str|Path='.', # Location of `df`, defaults to current working directory
        procs:list=None, # List of `TabularProc`s
        cat_names:list=None, # Column names pertaining to categorical variables
        cont_names:list=None, # Column names pertaining to continuous variables
        y_names:list=None, # Names of the dependent variables
        y_block:TransformBlock=None, # `TransformBlock` to use for the target(s)
        valid_idx:list=None, # List of indices to use for the validation set, defaults to a random split
        **kwargs
    ):
        "Create `TabularDataLoaders` from `df` in `path` using `procs`"
        if cat_names is None: cat_names = []
        if cont_names is None: cont_names = list(set(df)-set(L(cat_names))-set(L(y_names)))
        splits = RandomSplitter()(df) if valid_idx is None else IndexSplitter(valid_idx)(df)
        to = TabularPandas(df, procs, cat_names, cont_names, y_names, splits=splits, y_block=y_block)
        return to.dataloaders(path=path, **kwargs)

    @classmethod
    def from_csv(cls, 
        csv:str|Path|io.BufferedReader, # A csv of training data
        skipinitialspace:bool=True, # Skip spaces after delimiter
        **kwargs
    ):
        "Create `TabularDataLoaders` from `csv` file in `path` using `procs`"
        return cls.from_df(pd.read_csv(csv, skipinitialspace=skipinitialspace), **kwargs)

    @delegates(TabDataLoader.__init__)
    def test_dl(self, 
        test_items, # Items to create new test `TabDataLoader` formatted the same as the training data
        rm_type_tfms=None, # Number of `Transform`s to be removed from `procs`
        process:bool=True, # Apply validation `TabularProc`s to `test_items` immediately
        inplace:bool=False, # Keep separate copy of original `test_items` in memory if `False`
        **kwargs
    ):
        "Create test `TabDataLoader` from `test_items` using validation `procs`"
        to = self.train_ds.new(test_items, inplace=inplace)
        if process: to.process()
        return self.valid.new(to, **kwargs)

Tabular._dbunch_type = TabularDataLoaders
TabularDataLoaders.from_csv = delegates(to=TabularDataLoaders.from_df)(TabularDataLoaders.from_csv)
