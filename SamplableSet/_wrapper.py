# MIT License

# Copyright (c) 2018 Guillaume St-Onge

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from _SamplableSetCR import *

template_classes = {
    'int': IntSamplableSet,
    'edge': EdgeSamplableSet
}

class SamplableSet:
    """
    This class implements a set which is samplable in O(1) time according to the weight distribution of the elements. Elements can either be an integer or a tuple of 3 integers.

    The SamplableSet can be instanciated empty or from an iterable of 2 iterables of elements and weights respectively.

    This class is a wrapper around a C++ implementation.
    """
    def __init__(self, min_weight, max_weight, elements_weights=None, seed=None, cpp_type='int'):
        """
        Creates a new SamplableSet instance.

        Args:
            min_weight (float): Minimum weight a given element can have. This is needed for a good repartition of the elements inside the internal tree structure.
            max_weight (float): Maximum weight a given element can have. This is needed for a good repartition of the elements inside the internal tree structure.
            elements_weights (iterable of 2 iterables or dict, optional): If an iterable, should be a pair of 2 iterables of same lengths with which the set will be instanciated. The first iterable should be the elements and the second should be the respective weights. If a dict, keys should be the elements and values should be the weights. If not specified, the set will be empty.
            seed (float, optional): Seed used to sample elements from the set.
            cpp_type (str, optional, either 'int' or 'edge'): Type used in the C++ implementation. 'edge' should be a tuple of 3 integers. If 'elements_weights' is specified, the type will be infered from it.
        """
        # Unpacking
        if elements_weights:
            if isinstance(elements_weights, dict):
                elements = elements_weights.keys()
                weights = elements_weights.values()
            else:
                elements, weights = elements_weights

            # Infering cpp_type
            first_element = next(iter(elements))
            first_weight = next(iter(weights))
            cpp_type = 'int' if first_element is int else 'edge'

            # Validation
            if len(elements) != len(weights):
                raise ValueError("'elements' and 'weights' should have the same length.")

        # Instanciate the set
        if seed is None:
            self._samplable_set = template_classes[cpp_type](min_weight, max_weight)
        else:
            self._samplable_set = template_classes[cpp_type](min_weight, max_weight, seed)

        for func_name in ['size', 'total_weight', 'count', 'insert', 'set_weight', 'erase']:
            setattr(self, func_name, getattr(self._samplable_set, func_name))

        self.max_weight = max_weight
        self.min_weight = min_weight

        # Initialize the set
        if elements_weights:
            self[first_element] = first_weight
            for element, weight in zip(elements, weights):
                self[element] = weight

    def __contains__(self, element):
        return True if self.count(element) else False

    def __getitem__(self, element):
        return self.get_weight(element)

    def __setitem__(self, element, weight):
        if self.min_weight <= weight <= self.max_weight:
            if element in self:
                self.set_weight(element, weight)
            else:
                self.insert(element, weight)
        else:
            raise ValueError(f'Cannot assign weight outside range [{self.min_weight}, {self.max_weight}].')

    def __delitem__(self, element):
        self.erase(element)

    def __str__(self):
        return f'SamplableSet of {len(self)} element' + ('s' if len(self) > 1 else '')

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.size()

    def copy(self):
        return type(self._samplable_set)(self._samplable_set)

    def __deepcopy__(self, memo_dict):
        return self.copy()

    def __copy__(self):
        return self.copy()

    def sample(self, n_samples=1):
        """
        Randomly samples the set according to the weights of each element in O(1) time.

        Args:
            n_samples (int, optional): If equal to 1, returns one element. If greater than 1, returns a generator that will return 'n_samples' elements.

        Returns: An element of the set or a generator of 'n_samples' elements.
        """
        if n_samples == 1:
            return self._samplable_set.sample()
        else:
            return self.sample_generator(n_samples)

    def sample_generator(self, n_samples):
            for _ in range(n_samples):
                yield self._samplable_set.sample()
