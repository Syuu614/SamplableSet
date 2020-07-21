#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the initializaiton, insertion, sampling, etc. methods for samplable set

Author: Guillaume St-Onge <guillaume.st-onge.4@ulaval.ca>
"""

import pytest
import numpy as np
from SamplableSet import SamplableSet


class TestContainerModification:
    def test_clear(self):
        elements = ['a']
        weights = [33.3]
        elements_weights = zip(elements, weights)
        s = SamplableSet(1, 100, elements_weights)
        s.clear()
        assert s.total_weight() == 0 and len(s) == 0 and s.sample() is None and s.empty()

    def test_insert(self):
         s = SamplableSet(1, 10)
         s['a'] = 2.
         assert len(s) == 1 and not s.empty()

    def test_erase(self):
         s = SamplableSet(1, 10)
         s['a'] = 2.
         del s['a']
         assert len(s) == 0 and s.empty()

    def test_get_weight(self):
         s = SamplableSet(1, 10)
         s['a'] = 2.
         assert s['a'] == 2.

    def test_get_weight_no_item(self):
         s = SamplableSet(1, 10)
         s['a'] = 2.
         assert s['b'] is None

    def test_set_weight(self):
         s = SamplableSet(1, 10)
         s['a'] = 2.
         s['a'] = 3.
         assert s['a'] == 3. and len(s) == 1 and s.total_weight() == 3.

    def test_throw_error_1(self):
        with pytest.raises(ValueError):
            s = SamplableSet(1, 10)
            s['a'] = 0.5

    def test_throw_error_2(self):
        with pytest.raises(ValueError):
            s = SamplableSet(1, 10)
            s['a'] = 2.
            s['b'] = 0.5

    def test_throw_error_3(self):
        with pytest.raises(ValueError):
            s = SamplableSet(1, 10)
            s['a'] = 2.
            s['a'] = 11



class TestSampling:
    def test_sampling_single(self):
        elements = ['a']
        weights = [33.3]
        elements_weights = zip(elements, weights)
        s = SamplableSet(1, 100, elements_weights)
        element, weight = s.sample()
        assert element == 'a' and weight == 33.3 and len(s) == 1

    def test_sampling_generator(self):
        elements = ['a']
        weights = [33.3]
        elements_weights = zip(elements, weights)
        s = SamplableSet(1, 100, elements_weights)
        element_list = []
        weight_list = []
        for element, weight in s.sample(n_samples=5):
            element_list.append(element)
            weight_list.append(weight)
        assert element_list == ['a']*5 and weight_list == [33.3]*5 and len(s) == 1

    def test_sampling_no_replacement_single(self):
        elements = ['a']
        weights = [33.3]
        elements_weights = zip(elements, weights)
        s = SamplableSet(1, 100, elements_weights)
        element, weight = s.sample(replace=False)
        assert element == 'a' and weight == 33.3 and len(s) == 0

    def test_sampling_no_replacement_generator(self):
        elements = ['a']
        weights = [33.3]
        elements_weights = zip(elements, weights)
        s = SamplableSet(1, 100, elements_weights)
        sample_list = []
        for sample in s.sample(n_samples=5,replace=False):
            sample_list.append(sample)
        assert sample_list == [('a',33.3),None,None,None,None] and len(s) == 0


class TestInitialization:
    def test_dict_init(self):
        elements_weights = {3:33.3, 6:66.6}
        s = SamplableSet(1, 100, elements_weights)
        assert 3 in s and 6 in s

    def test_iterable_init(self):
        elements = ['a', 'b']
        weights = [33.3, 66.6]
        elements_weights = zip(elements, weights)
        s = SamplableSet(1, 100, elements_weights)
        assert 'a' in s and 'b' in s

    def test_empty_init(self):
        s = SamplableSet(1,100)
        assert s.cpp_type is None
        s['a'] = 2.
        assert s.cpp_type == 'str'
        assert len(s) == 1 and s['a'] == 2.

    def test_throw_error_1(self):
        with pytest.raises(ValueError):
            s = SamplableSet(0, 100)

    def test_throw_error_2(self):
        with pytest.raises(ValueError):
            s = SamplableSet(1, np.inf)

    def test_throw_error_3(self):
        with pytest.raises(ValueError):
            s = SamplableSet(2, 1)



