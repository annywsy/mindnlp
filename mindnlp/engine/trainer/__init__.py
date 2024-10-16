'''Copyright 2022 Huawei Technologies Co., Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
============================================================================'''

# pylint: disable= line-too-long

from typing import TYPE_CHECKING
from .base import Trainer
from ...trl.import_utils import _LazyModule, is_diffusers_available, OptionalDependencyNotAvailable


_import_structure = {
    "utils": [
        "AdaptiveKLController",
        "FixedKLController",
        "ConstantLengthDataset",
        "DataCollatorForCompletionOnlyLM",
        "RunningMoments",
        "disable_dropout_in_model",
        "peft_module_casting_to_bf16",
        "RichProgressCallback",
    ],

    "dpo_trainer": ["DPOTrainer"],
    "cpo_trainer": ["CPOTrainer"],
    "alignprop_trainer": ["AlignPropTrainer"],
    "iterative_sft_trainer": ["IterativeSFTTrainer"],
    "orpo_trainer": ["ORPOTrainer"],
    "ppo_trainer": ["PPOTrainer"],
    "reward_trainer": ["RewardTrainer", "compute_accuracy"],
    "sft_trainer": ["SFTTrainer"],
    "base": ["BaseTrainer"],
    # "ddpo_config": ["DDPOConfig"],
}

try:
    if not is_diffusers_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    pass
else:
    _import_structure["ddpo_trainer"] = ["DDPOTrainer"]


if TYPE_CHECKING:
    # isort: off
    from .utils import (
        AdaptiveKLController,
        FixedKLController,
        ConstantLengthDataset,
        DataCollatorForCompletionOnlyLM,
        RunningMoments,
        disable_dropout_in_model,
        peft_module_casting_to_bf16,
        RichProgressCallback,
    )

    # isort: on

    from .base import BaseTrainer
    # from .dpo_trainer import DPOTrainer
    # from .iterative_sft_trainer import IterativeSFTTrainer
    # from .cpo_trainer import CPOTrainer
    from .kto_trainer import KTOTrainer
    # from .ppo_trainer import PPOTrainer
    from .reward_trainer import RewardTrainer, compute_accuracy
    from .sft_trainer import SFTTrainer

    # try:
    #     if not is_diffusers_available():
    #         raise OptionalDependencyNotAvailable()
    # except OptionalDependencyNotAvailable:
    #     pass
    # else:
    #     from .ddpo_trainer import DDPOTrainer
else:
    import sys

    sys.modules[__name__] = _LazyModule(__name__, globals()["__file__"], _import_structure, module_spec=__spec__)
