#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The OutputData Pattern."""

from .pattern import Pattern, pattern_registry
from collections import namedtuple, OrderedDict
from .. import graph_utils as util
import copy


@pattern_registry(pattern_type='OutputData')
class OutputData(Pattern):
    """The OutputData pattern.

    Fuse the original sub-graph into the custom acceleration 'OutputData' graph.
    The search strategy is based on the following pattern mapping configs for different models.
    """
    def __call__(self, model):
        """The __call__ function of this pattern class."""
        # make the output_data node in graph
        model_output_tensors = []
        for node in model.nodes:
            for output_tensor in node.output_tensors:
                if not output_tensor.dest_op:
                    model_output_tensors.append(copy.deepcopy(output_tensor))
        output_data_node = util.construct_node('output_data',
                                               'Output',
                                               input_tensors=model_output_tensors)
        model.insert_nodes(len(model.nodes), [output_data_node])
        model.nodes[-1].attr = None

        return model
