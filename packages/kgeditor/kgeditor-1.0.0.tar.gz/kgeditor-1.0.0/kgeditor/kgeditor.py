from .one_shot_learner import OneShotLearner
from higher.patch import monkeypatch as make_functional
import torch  
'''
param of OneShotLearner:
    model,
    vocab_dim=30522,
    embedding_dim=768,
    hidden_dim=128,
    condition_dim=1024,
    include_set={},
    max_scale=1e-3,
    embedding_init=None,
'''

class KGEditor(object):
    def __init__(self, *args):
        self.ex_learner = OneShotLearner(args) # problem: where to add learner's optimizer
        self.args = args
        self.ex_model = args.model
    
    def get_logits_orig_params_dict(self, batch):
        '''
        params:
            edit_num,
            
        '''
        with torch.enable_grad():
            logits = self.ex_model.eval()(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                token_type_ids=batch["token_type_ids"],
            ).logits
            
            logits_orig, _ = logits.split([
                len(batch["input_ids"]) - self.args.edit_num,
                self.args.edit_num,
            ])
            
            #  get the info of gradient
            grads = torch.autograd.grad(
                # cross_entropy
                torch.nn.functional.cross_entropy(
                    logits[-self.args.edit_num:, :],
                    batch["label"][-self.args.edit_num:],
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
        