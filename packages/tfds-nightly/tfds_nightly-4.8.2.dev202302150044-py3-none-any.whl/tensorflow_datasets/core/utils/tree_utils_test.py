# coding=utf-8
# Copyright 2022 The TensorFlow Datasets Authors.
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

"""Tests for tree_utils."""

import pytest
from tensorflow_datasets.core.utils import tree_utils


def test_tree_parallel_map():
  assert tree_utils.parallel_map(
      lambda x: x * 10, {'a': [1, 2, 3], 'b': [4, 5]}
  ) == {'a': [10, 20, 30], 'b': [40, 50]}


def test_tree_parallel_map_reraise():
  def fn(x):
    raise ValueError('Bad value')

  with pytest.raises(ValueError, match='Bad value'):
    tree_utils.parallel_map(fn, [1])
