import math
import os
import numpy as np
from copy import deepcopy
from higher.patch import monkeypatch as make_functional
import pytorch_lightning as pl
import torch
from pytorch_lightning import LightningModule
from torch.utils.data import DataLoader
from transformers import (
    get_linear_schedule_with_warmup,
    AutoConfig,
)

from src.models.one_shot_learner import OneShotLearner
from src.models.modeling_bert import bert_mapping

from src.data.data_module import dataset_mapping

class Args:
  def __init__(self, **entries) -> None:
      self.__dict__.update(entries)

class BaseModel(LightningModule):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.save_hyperparameters()
        
        config = AutoConfig.from_pretrained(
            self.hparams.ex_model_checkpoint,
        )
        
        config.ex_size = self.hparams.ex_size
        config.kb_layer = [int(i) for i in self.hparams.kb_layer.split(',') if i != '']
        
        self.ex_model = bert_mapping[kwargs['kge_model_type']].from_pretrained(
            self.hparams.ex_model_checkpoint, config=config).eval()
        
        data = dataset_mapping[kwargs['kge_model_type']](Args(**kwargs))
        data.setup()

        self.__dict__.update(data.get_config())
        
        self.task_name = kwargs['task_name']

        self.params = {}
        
        self.epoch = 0
        self.edit_num = kwargs['edit_num']
        
        self.ex_learner = OneShotLearner(
            self.ex_model,
            vocab_dim=self.ex_model.bert.embeddings.word_embeddings.weight.data.
            shape[0],
            embedding_dim=self.ex_model.bert.embeddings.word_embeddings.weight.
            data.shape[1],
            hidden_dim=128,
            condition_dim=1024,
            include_set={
                n
                for n, _ in self.ex_model.named_parameters()
                if ("dense_in_ex" in n.lower() or "dense_out_ex" in n.lower()) and "bias" not in n.lower()
            },
            max_scale=self.hparams.max_scale,
            embedding_init=self.ex_model.bert.embeddings.word_embeddings.weight.
            data,
        )
        
        self.alpha_kl = torch.nn.Parameter(torch.ones(()))
        self.alpha_kl.register_hook(lambda grad: -grad)

        self.alpha_lp = torch.nn.Parameter(torch.ones(()))
        self.alpha_lp.register_hook(lambda grad: -grad)

        self.train_acc = pl.metrics.Accuracy()
        self.valid_acc = pl.metrics.Accuracy()
        self.valid_flipped = pl.metrics.Accuracy()

        self.register_buffer("margin_kl",
                             torch.tensor(self.hparams.margin_kl_max))
        self.register_buffer("margin_lp",
                             torch.tensor(self.hparams.margin_lp_max))
        self.running_flipped = []

    def train_dataloader(self, shuffle=True):
        return DataLoader(
            self.data_train,
            batch_size=self.hparams.edit_num,
            collate_fn=self.sampler,
            num_workers=self.hparams.num_workers,
            shuffle=shuffle,
            drop_last=True
        )

    def val_dataloader(self, shuffle=False):
        
        pass
        
    def get_logits_orig_params_dict(self, batch):
      
        pass
      
    def forward(self, batch, logits_orig=None, params_dict=None):

        pass
    
    def get_kl_lp_cr(self, logits_orig, logits, label, params_dict, input_ids):
        
        pass

    def validation_step(self, batch, batch_idx=None):

        result = self._eval(batch, batch_idx)
        return result
    
    def _eval(self, batch, batch_idx, ):
        
        pass
    
    def validation_epoch_end(self, outputs):
        if self.epoch % 5 == 0:
          torch.save(self.ex_learner, f"./output/{str(self.hparams.kge_model_type) + '_' + str(self.task_name)}/{str(self.epoch)}_params.pt")

        self.epoch = self.epoch + 1
        
        loc_ranks = np.concatenate([_['ranks'][:-self.edit_num] for _ in outputs])
        edit_ranks = np.concatenate([_['ranks'][-self.edit_num:] for _ in outputs])

        loc_hits5 = (loc_ranks<=5).mean()
        loc_hits3 = (loc_ranks<=3).mean()
        loc_hits1 = (loc_ranks<=1).mean()
        edit_hits5 = (edit_ranks<=5).mean()
        edit_hits3 = (edit_ranks<=3).mean()
        edit_hits1 = (edit_ranks<=1).mean()
        print("Eval/ranks", edit_ranks)
        print("Eval/hits5", edit_hits5)
        print("Eval/hits3", edit_hits3)
        print("Eval/hits1", edit_hits1)
        print("Eval/mean_rank", edit_ranks.mean())
        print("Eval/mrr", (1. / edit_ranks).mean())
        print("Eval/loc_hits1", loc_hits1)
        print("Eval/loc_hits3", loc_hits3)
        print("Eval/loc_hits5", loc_hits5)
        print("Eval/loc_mean_rank", loc_ranks.mean())
        print("Eval/loc_mrr", (1. / loc_ranks).mean())

        self.log("Eval/loc_hits1", loc_hits1)
        self.log("Eval/loc_hits3", loc_hits3)
        self.log("Eval/loc_hits5", loc_hits5)
        self.log("Eval/loc_mean_rank", loc_ranks.mean())
        self.log("Eval/loc_mrr", (1. / loc_ranks).mean())
        self.log("Eval/hits5", edit_hits5)
        self.log("Eval/hits3", edit_hits3)
        self.log("Eval/hits1", edit_hits1)
        self.log("Eval/mean_rank", edit_ranks.mean())
        self.log("Eval/mrr", (1. / edit_ranks).mean())
        
        return super().validation_epoch_end(outputs)
        

    def sample(
        self,
        sentences,
        condition,
        logits_orig=None,
        params_dict=None,
        stop_condition=None,
    ):
        len_sent = len(sentences)
        with torch.no_grad():
            logits_orig, logits, params_dict = self.forward(
                {
                    k: v.to(self.device)
                    for k, v in self.val_dataset.get_batch(
                        sentences, condition).items()
                },
                logits_orig=logits_orig,
                params_dict=params_dict,
            )

            n_iter = 1
            if stop_condition is not None and stop_condition(
                    condition, logits, n_iter):
                model_tmp = deepcopy(self.model)
                params_dict_tmp = deepcopy(params_dict)

                while stop_condition(condition, logits, n_iter):
                    for n, p in self.model.named_parameters():
                        p.data += params_dict.get(n, 0)

                    _, logits, params_dict = self.forward({
                        k: v.to(self.device)
                        for k, v in self.val_dataset.get_batch(
                            sentences, condition).items()
                    })
                    params_dict_tmp = {
                        k: v + params_dict[k]
                        for k, v in params_dict_tmp.items()
                    }
                    n_iter += 1

                self.model = model_tmp
                params_dict = params_dict_tmp

            return logits_orig, logits[:len_sent], params_dict

    def on_before_zero_grad(self, optimizer):
        self.alpha_kl.data = torch.where(
            self.alpha_kl.data < 0,
            torch.full_like(self.alpha_kl.data, 0),
            self.alpha_kl.data,
        )
        self.alpha_lp.data = torch.where(
            self.alpha_lp.data < 0,
            torch.full_like(self.alpha_lp.data, 0),
            self.alpha_lp.data,
        )

    def configure_optimizers(self):
        optimizer = torch.optim.RMSprop(
            [
                {
                    "params": self.ex_learner.parameters(),
                    "lr": self.hparams.lr,
                },
                {
                    "params": [self.alpha_kl, self.alpha_lp],
                    "lr": self.hparams.lr_alpha,
                },
            ],
            centered=True,
        )

        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.hparams.warmup_updates,
            num_training_steps=self.hparams.total_num_updates,
        )

        return [optimizer], [{
            "scheduler": scheduler,
            "interval": "step",
            "frequency": 1
        }]

class FTModel(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def val_dataloader(self, shuffle=False):
        return DataLoader(
            self.data_val,
            batch_size=self.hparams.edit_num,
            collate_fn=self.test_sampler,
            num_workers=self.hparams.num_workers,
            shuffle=shuffle,
            drop_last=True
        )

    def get_logits_orig_params_dict(self, batch):

        with torch.enable_grad():
            logits = self.ex_model.eval()(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                token_type_ids=batch["token_type_ids"],
            ).logits
            
            logits_orig, _ = logits.split([
                len(batch["input_ids"]) - self.edit_num,
                self.edit_num,
            ])
            
            #  get the info of gradient
            grads = torch.autograd.grad(
                # cross_entropy
                torch.nn.functional.cross_entropy(
                    logits[-self.edit_num:, :],
                    batch["label"][-self.edit_num:],
                    reduction="none",
                ).mean(-1),
                self.ex_model.parameters(),
            )

        grads = {
            name: grad
            for (name, _), grad in zip(self.ex_model.named_parameters(), grads)
        }

        params_dict = self.ex_learner(
            batch["cond_input_ids"][-self.edit_num:],
            batch["cond_attention_mask"][-self.edit_num:],
            grads=grads,
        )

        return logits_orig.detach(), params_dict
      
    def forward(self, batch, logits_orig=None, params_dict=None):

        if not params_dict:
            logits_orig, params_dict = self.get_logits_orig_params_dict(batch)

        fmodel = make_functional(self.ex_model).eval()

        logits = fmodel(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            token_type_ids=batch["token_type_ids"],
            # add delta theta
            params=[
                params_dict.get(n, 0) + p
                for n, p in self.ex_model.named_parameters()
            ],
        ).logits

        return logits_orig, logits, params_dict
    
    def get_kl_lp_cr(self, logits_orig, logits, label, params_dict, input_ids):
        kl = torch.distributions.kl_divergence(
            torch.distributions.Categorical(torch.nn.functional.softmax(logits_orig)),
            torch.distributions.Categorical(
               torch.nn.functional.softmax(logits[:-self.edit_num])),
        )
        
        # don't update too much params
        lp = sum((p.abs()**self.hparams.p).mean()**(1 / self.hparams.p)
                 for p in params_dict.values()) / len(params_dict)

        # ensure the result which has been edited
        cr = torch.nn.functional.cross_entropy(
            logits[-self.edit_num:],
            label[-self.edit_num:],
            reduction="none",
        ).mean(-1)

        return kl, lp, cr

    def training_step(self, batch, batch_idx=None):

        logits_orig, logits, params_dict = self.forward(batch)

        kl, lp, cr = self.get_kl_lp_cr(logits_orig, logits, batch['label'],
                                       params_dict, batch["input_ids"])
        kl = kl.mean(-1) 
        
        loss_kl = self.alpha_kl * (kl)
        loss_lp = self.alpha_lp * (lp - self.margin_lp)

        if self.hparams.divergences == "both":
            loss = cr + loss_kl + loss_lp
        elif self.hparams.divergences == "kl":
            loss = cr + loss_kl
        elif self.hparams.divergences == "lp":
            loss = cr + loss_lp

        self.log("alpha_kl",
                 self.alpha_kl,
                 on_step=True,
                 on_epoch=False,
                 prog_bar=True)
        self.log("alpha_lp",
                 self.alpha_lp,
                 on_step=True,
                 on_epoch=False,
                 prog_bar=True)
        self.log("kl", kl, on_step=True, on_epoch=False, prog_bar=True)
        self.log("lp", lp, on_step=True, on_epoch=False, prog_bar=True)
        self.log("cr", cr, on_step=True, on_epoch=False, prog_bar=True)

        return {"loss": torch.abs(loss)}
    
    def _eval(self, batch, batch_idx, ):
        logits_orig, params_dict = self.get_logits_orig_params_dict(batch)
        fmodel = make_functional(self.ex_model).eval()
        input_ids = batch['input_ids'] 

        logits = fmodel(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            token_type_ids=batch["token_type_ids"],
            # add delta theta
            params=[
                params_dict.get(n, 0) + p
                for n, p in self.ex_model.named_parameters()
            ],
        ).logits
        
        all_rank = []
        for cur_batch in range(input_ids.shape[0]):
            preds = []
            preds.append(logits[cur_batch, 1].item())
            cur_input_ids = []
            cur_attention_mask = []
            cur_token_type_ids = []
            for idx in range(len(batch["cor_triples_input_ids"][cur_batch])):
                if (idx + 1) % 128 == 0 or ((idx + 128) > len(batch["cor_triples_input_ids"][cur_batch]) and idx == len(batch["cor_triples_input_ids"][cur_batch]) - 1):
                    if len(cur_input_ids) == 0:
                        continue
                    cur_input_ids = torch.tensor(cur_input_ids).to("cuda")
                    cur_attention_mask = torch.tensor(cur_attention_mask).to("cuda")
                    cur_token_type_ids = torch.tensor(cur_token_type_ids).to("cuda")
                    fmodel = make_functional(self.ex_model).eval()
                    cur_logits = fmodel(
                        input_ids=cur_input_ids if len(cur_input_ids.shape) == 2 else cur_input_ids.unsqueeze(dim=0),
                        attention_mask=cur_attention_mask if len(cur_attention_mask.shape) == 2 else cur_attention_mask.unsqueeze(dim=0),
                        token_type_ids=cur_token_type_ids if len(cur_token_type_ids.shape) == 2 else cur_token_type_ids.unsqueeze(dim=0),
                        # add delta theta
                        params=[
                            # p
                            params_dict.get(n, 0) + p
                            for n, p in self.ex_model.named_parameters()
                        ],
                    ).logits

                    preds += [cur_logits[i, 1].item() for i in range(cur_logits.shape[0])]
                    cur_input_ids = []
                    cur_attention_mask = []
                    cur_token_type_ids = []
                else:
                    cur_input_ids.append(batch["cor_triples_input_ids"][cur_batch][idx])
                    cur_attention_mask.append(batch["cor_triples_attention_mask"][cur_batch][idx])
                    cur_token_type_ids.append(batch["cor_triples_token_type_ids"][cur_batch][idx])

            preds = torch.tensor(preds)
            _, rank_list = torch.sort(preds, descending=True)
            rank = torch.where(rank_list == 0)[0][0].item() + 1
            all_rank.append(rank)
        
        return dict(ranks = np.array(all_rank))

class PTModel(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def val_dataloader(self, shuffle=False):
        return DataLoader(
            self.data_val,
            batch_size=self.hparams.edit_num,
            collate_fn=self.sampler,
            num_workers=self.hparams.num_workers,
            shuffle=shuffle,
            drop_last=True
        )

    def get_logits_orig_params_dict(self, batch):

        with torch.enable_grad():
            logits = self.ex_model.eval()(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
            ).logits
            
            logits_orig, _ = logits.split([
                len(batch["input_ids"]) - self.edit_num,
                self.edit_num,
            ])
            input_ids = batch['input_ids']
            batch_idx, mask_idx = (input_ids == self.tokenizer.mask_token_id).nonzero(as_tuple=True)
            mask_logits = logits[batch_idx, mask_idx, self.entity_id_st:self.entity_id_ed]
            
            #  get info of gradient
            grads = torch.autograd.grad(
                # cross_entropy
                torch.nn.functional.cross_entropy(
                    mask_logits[-self.edit_num:, :],
                    batch["label"][-self.edit_num:],
                    reduction="none",
                ).mean(-1),
                self.ex_model.parameters(),
            )

        grads = {
            name: grad
            for (name, _), grad in zip(self.ex_model.named_parameters(), grads)
        }

        params_dict = self.ex_learner(
            batch["cond_input_ids"][-self.edit_num:],
            batch["cond_attention_mask"][-self.edit_num:],
            grads=grads,
        )

        return logits_orig.detach()[:, :, self.entity_id_st:self.entity_id_ed], params_dict

    def forward(self, batch, logits_orig=None, params_dict=None):

        if not params_dict:
            logits_orig, params_dict = self.get_logits_orig_params_dict(batch)

        fmodel = make_functional(self.ex_model).eval()

        logits = fmodel(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            # add delta theta
            params=[
                params_dict.get(n, 0) + p
                for n, p in self.ex_model.named_parameters()
            ],
        ).logits
        
        return logits_orig, logits[:, :, self.entity_id_st:self.entity_id_ed], params_dict
    
    def get_kl_lp_cr(self, logits_orig, logits, label, params_dict, input_ids):
        # Reliability
        pos = (input_ids == self.tokenizer.mask_token_id).nonzero(as_tuple=True)
        # 
        kl = torch.distributions.kl_divergence(
            torch.distributions.Categorical(torch.nn.functional.softmax(logits_orig[pos[0][:-self.edit_num], pos[1][:-self.edit_num], :])),
            torch.distributions.Categorical(
               torch.nn.functional.softmax(logits[pos[0][:-self.edit_num], pos[1][:-self.edit_num], :])),
        )
        
        # don't update too much params
        lp = sum((p.abs()**self.hparams.p).mean()**(1 / self.hparams.p)
                 for p in params_dict.values()) / len(params_dict)

        # ensure the result which has been edited
        cr = torch.nn.functional.cross_entropy(
            logits[pos[0][-self.edit_num:], pos[1][-self.edit_num:], :],
            label[-self.edit_num:],
            reduction="none",
        ).mean(-1)

        return kl, lp, cr

    def training_step(self, batch, batch_idx=None):

        logits_orig, logits, params_dict = self.forward(batch)

        kl, lp, cr = self.get_kl_lp_cr(logits_orig, logits, batch['label'],
                                       params_dict, batch["input_ids"])
        kl = kl.mean(-1) 

        loss_kl = self.alpha_kl * (kl - self.margin_kl) # margin_kl is too large
        loss_lp = self.alpha_lp * (lp - self.margin_lp)

        if self.hparams.divergences == "both":
            loss = cr + loss_kl + loss_lp
        elif self.hparams.divergences == "kl":
            loss = cr + loss_kl
        elif self.hparams.divergences == "lp":
            loss = cr + loss_lp

        self.log("alpha_kl",
                 self.alpha_kl,
                 on_step=True,
                 on_epoch=False,
                 prog_bar=True)
        self.log("alpha_lp",
                 self.alpha_lp,
                 on_step=True,
                 on_epoch=False,
                 prog_bar=True)
        self.log("kl", kl, on_step=True, on_epoch=False, prog_bar=True)
        self.log("lp", lp, on_step=True, on_epoch=False, prog_bar=True)
        self.log("cr", cr, on_step=True, on_epoch=False, prog_bar=True)

        return {"loss": torch.abs(loss)}

    def _eval(self, batch, batch_idx, ):
        logits_orig, params_dict = self.get_logits_orig_params_dict(batch)
        fmodel = make_functional(self.ex_model).eval()
        input_ids = batch['input_ids']
        # single label
        label = batch.pop('label')
        my_keys = list(batch.keys())
        for k in my_keys:
            if k not in ["input_ids", "attention_mask", "token_type_ids"]:
                batch.pop(k)    
        
        logits = fmodel(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            # add delta theta
            params=[
                params_dict.get(n, 0) + p
                for n, p in self.ex_model.named_parameters()
            ],
        ).logits[:, :, self.entity_id_st:self.entity_id_ed]
        
        _, mask_idx = (input_ids == self.tokenizer.mask_token_id).nonzero(as_tuple=True)
        bsz = input_ids.shape[0]
        logits = logits[torch.arange(bsz), mask_idx]

        _, outputs = torch.sort(logits, dim=1, descending=True) # outputs代表
        edit_entity_order = outputs[-self.edit_num:, :]
        edit_input_ids = batch["input_ids"][-self.edit_num:, :]
        edit_labels = label[-self.edit_num:]
        _, outputs = torch.sort(outputs, dim=1)
        ranks = outputs[torch.arange(bsz), label].detach().cpu() + 1
        edit_ranks = ranks[-self.edit_num:]
        
        return dict(ranks = np.array(ranks), edit_entity_order = np.array(edit_entity_order.detach().cpu()), edit_input_ids = edit_input_ids, edit_labels = edit_labels, edit_ranks = edit_ranks)

model_mapping = {
    'FT': FTModel,
    'PT': PTModel,
}