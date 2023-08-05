# Copyright 2022 The Orbax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines exported symbols for the `orbax` packageorbax.checkpoint."""

import functools

from orbax_checkpoint import checkpoint_utils
from orbax_checkpoint import lazy_utils
from orbax_checkpoint import test_utils
from orbax_checkpoint import type_handlers
from orbax_checkpoint.abstract_checkpointer import AbstractCheckpointer
from orbax_checkpoint.array_checkpoint_handler import ArrayCheckpointHandler
from orbax_checkpoint.async_checkpoint_handler import AsyncCheckpointHandler
from orbax_checkpoint.async_checkpointer import AsyncCheckpointer
from orbax_checkpoint.checkpoint_handler import CheckpointHandler
from orbax_checkpoint.checkpoint_manager import CheckpointManager
from orbax_checkpoint.checkpoint_manager import CheckpointManagerOptions
from orbax_checkpoint.checkpointer import Checkpointer
from orbax_checkpoint.future import Future
from orbax_checkpoint.json_checkpoint_handler import JsonCheckpointHandler
from orbax_checkpoint.pytree_checkpoint_handler import ArrayRestoreArgs
from orbax_checkpoint.pytree_checkpoint_handler import PyTreeCheckpointHandler
from orbax_checkpoint.pytree_checkpoint_handler import RestoreArgs
from orbax_checkpoint.pytree_checkpoint_handler import SaveArgs
from orbax_checkpoint.transform_utils import apply_transformations
from orbax_checkpoint.transform_utils import Transform

# Convenient shorthand where instead of the following:
#   `checkpointer = Checkpointer(PyTreeCheckpointer())`
# we can just use:
#   `checkpointer = PyTreeCheckpointer()`
PyTreeCheckpointer = functools.partial(Checkpointer, PyTreeCheckpointHandler())

# A new PyPI release will be pushed everytime `__version__` is increased.
__version__ = '0.1.1'
