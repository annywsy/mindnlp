'''Copyright 2024 The HuggingFace Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

# pylint: disable= line-too-long
# pylint: disable= too-many-instance-attributes

from dataclasses import dataclass, field
from typing import List, Optional

from mindnlp.engine import TrainingArguments

from ...trl.core import flatten_dict

@dataclass
class RewardConfig(TrainingArguments):
    """
    RewardConfig collects all training arguments related to the [`RewardTrainer`] class.

    Using [`HfArgumentParser`] we can turn this class into
    [argparse](https://docs.python.org/3/library/argparse#module-argparse) arguments that can be specified on the
    command line.

    Parameters:
        max_length (`int`, *optional*, defaults to `None`):
            The maximum length of the sequences in the batch. This argument is required if you want to use the default data collator.
        gradient_checkpointing (`bool`, *optional*, defaults to `True`):
                If True, use gradient checkpointing to save memory at the expense of slower backward pass.
    """

    max_length: Optional[int] = None
    """The maximum length of the sequences in the batch. This argument is required if you want to use the default data collator."""


    model_name_or_path: Optional[str] = field(
        default=None,
        metadata={"help": ("The model checkpoint for weights initialization.")},
    )
    model_revision: str = field(
        default="main",
        metadata={"help": "The specific model version to use (can be a branch name, tag name or commit id)."},
    )

    trust_remote_code: bool = field(default=False, metadata={"help": "Trust remote code when loading a model."})
    attn_implementation: Optional[str] = field(
        default=None,
        metadata={
            "help": (
                "Which attention implementation to use; you can run --attn_implementation=flash_attention_2, in which case you must install this manually by running `pip install flash-attn --no-build-isolation`"
            )
        },
    )
    use_peft: bool = field(
        default=False,
        metadata={"help": ("Whether to use PEFT or not for training.")},
    )
    lora_r: Optional[int] = field(
        default=16,
        metadata={"help": ("LoRA R value.")},
    )
    lora_alpha: Optional[int] = field(
        default=32,
        metadata={"help": ("LoRA alpha.")},
    )
    lora_dropout: Optional[float] = field(
        default=0.05,
        metadata={"help": ("LoRA dropout.")},
    )
    lora_target_modules: Optional[List[str]] = field(
        default=None,
        metadata={"help": ("LoRA target modules.")},
    )
    lora_modules_to_save: Optional[List[str]] = field(
        default=None,
        metadata={"help": ("Model layers to unfreeze & train")},
    )
    lora_task_type: str = field(
        default="CAUSAL_LM", metadata={"help": "The task_type to pass for LoRA (use SEQ_CLS for reward modeling)"}
    )
    load_in_8bit: bool = field(
        default=False, metadata={"help": "use 8 bit precision for the base model - works only with LoRA"}
    )
    load_in_4bit: bool = field(
        default=False, metadata={"help": "use 4 bit precision for the base model - works only with LoRA"}
    )

    bnb_4bit_quant_type: Optional[str] = field(
        default="nf4", metadata={"help": "precise the quantization type (fp4 or nf4)"}
    )
    use_bnb_nested_quant: bool = field(default=False, metadata={"help": "use nested quantization"})

    def to_dict(self):
        output_dict = {}
        for key, value in self.__dict__.items():
            output_dict[key] = value
        return flatten_dict(output_dict)

    def __post_init__(self):
        if self.load_in_8bit and self.load_in_4bit:
            raise ValueError("You can't use 8 bit and 4 bit precision at the same time")

        if isinstance(self.lora_target_modules, list) and len(self.lora_target_modules) == 1:
            self.lora_target_modules = self.lora_target_modules[0]
    