"""extendable_str module, provides an ExtendStr class optimized for frequent appending

The module contains one class: ExtendableStr

English version is translated by DeepSeek
"""

from collections.abc import Sequence
from functools import singledispatch
from typing import Any, Self

__all__ = [
    'ExtendableStr',
]
__license__ = 'MIT license'
__author__ = 'YGSMT'

class ExtendableStr(Sequence):
    """String optimized for frequent appending and infrequent reading
    
    ExtendableStr inherits from collections.abc.Sequence
    
    Creating new instances:
    -------
    
    1. Create empty instance
    >>> es = ExtendableStr()
    
    2. Create from initial string
    >>> es = ExtendableStr('Sangonomiya Kokomi')
    
    3. Create from initial sequence (converts all elements to strings)
    >>> es = ExtendableStr([0, 'a', range(5)])
    >>> es = ExtendableStr((0, 'a', range(5)))
    >>> es = ExtendableStr(range(5))
    
    4. Create from other types (converts to string)
    >>> es = ExtendableStr(0)
    
    Adding chunks:
    ----
    
    5. Add single chunk
    Note: Use extend(seq) method to add a sequence (except strings)!
    >>> es = ExtendableStr()    # Create new instance
    >>> es.append('abc')
    >>> print(es)
    abc
    >>> es.append(0)
    >>> print(es)
    abc0
    
    6. Add multiple chunks (add sequence)
    >>> es = ExtendableStr()    # Create new instance
    >>> tmp = ExtendableStr(list('tmp'))
    >>> es.extend([1, 2, 3])
    >>> es
    ExtendableStr('123')    # within 3 blocks
    >>> es + tmp    # ExtendableStr instances add each chunk separately
    ExtendableStr('123tmp')    # within 6 blocks
    >>> es.extend(range(5))
    >>> es
    ExtendableStr('12301234')    # within 8 blocks
    >>> es.extend('abc')    # String added as whole chunk
    >>> es
    ExtendableStr('12301234abc')    # within 9 blocks
    
    Overflow consolidation limit:
    -------
    
    When chunk count exceeds given limit, merges all chunks into a single string
    Overflow limit disabled by default. To enable, pass integer ≥2 to overflow parameter during initialization. Raises ValueError if <2.
    
    7. Overflow limit reduces performance waste from excessive chunks
    >>> es = ExtendableStr(overflow=5)    # Create instance with max 5 chunks
    >>> es.append('Kokomi')
    >>> es
    ExtendableStr('Kokomi')    # within 1 blocks
    >>> es.extend([1, 2, 3])
    >>> es
    ExtendableStr('Kokomi123')    # within 4 blocks
    >>> es.extend(range(5))
    >>> # Overflow limit triggered, all chunks merged
    >>> es
    ExtendableStr('Kokomi12301234')    # within 1 blocks
    
    Manual consolidation:
    -----
    
    8. Manually consolidate instance
    >>> es = ExtendableStr()    # Create new instance
    >>> es.extend(range(5))
    >>> es
    ExtendableStr('01234')    # within 5 blocks
    >>> es.overflow()
    >>> es
    ExtendableStr('01234')    # within 1 blocks
    
    Sequence methods:
    -----
    
    9. len() returns string length without concatenation
    >>> es = ExtendableStr()    # Create new instance
    >>> es.append('Sangonomiya')
    >>> # Strings still not concatenated
    >>> len(es)
    11
    >>> es.append(' Kokomi')
    >>> len(es)
    18
    >>> # Still no concatenation occurred
    >>> print(es)    # First concatenation
    Sangonomiya Kokomi
    
    10. getitem() returns specific string items
    Integer index returns single character
    Slice returns ExtendableStr with result
    >>> es = ExtendableStr()    # Create new instance
    >>> es.append('Sangonomiya Kokomi')
    >>> es[0]
    'S'
    >>> es[-6:]
    ExtendableStr('Kokomi')    # within 1 blocks
    
    11. Other methods
    >>> es = ExtendableStr()    # Create new instance
    >>> es.append('Sangonomiya Kokomi')
    
    in operator (automatically converts left operand to string)
    >>> 'Kokomi' in es
    True
    
    __iter__()
    >>> for i in es:
    ...     print(i, end=' ')
    S a n g o n o m i y a   K o k o m i 
    
    __reversed__()
    >>> for i in reversed(es):
    ...     print(i, end='')
    imokoK ayimonognaS
    
    index()
    >>> es.index('a')
    1
    
    count()
    >>> es.count('o')
    4
    """
    
    def __init__(self, seq: Sequence | None = None,
                 overflow: int | None = None):
        """
        Parameters:
            seq: Sequence type
                Sequence elements converted to strings as initial content
                Can be empty. Default creates empty instance
                Non-sequence types converted to string as initial chunk (not recommended unless intentional)
            overflow: Integer type
                Overflow consolidation limit. Triggers consolidation when chunk count exceeds this value
                Must be ≥2, otherwise raises ValueError
                Default: None (feature disabled)
                Can manually call overflow() even when None
        """
        if seq is None:
            self.__data = []
        else:
            if isinstance(seq, str):
                self.__data = [seq]
            elif isinstance(seq, ExtendableStr):
                self.__data = seq._data[:]
            elif isinstance(seq, Sequence):
                self.__data = [str(i) for i in seq]
            else:
                self.__data = [str(seq)]
        self.__str = ''
        self.__formated = False
        self.__length = 0
        self.__measured = False
        if overflow is None:
            self.__overflow = 0
        elif overflow < 2:    # Must be greater than 1
            raise ValueError(f'Overflow limit must be >1, got {overflow}')
        else:
            self.__overflow = overflow
    
    @property
    def _data(self):
        """Return internal state (not intended for user use)"""
        
        return self.__data
    
    def __str__(self):
        """Return internal string representation"""
        
        self._to_str()
        return self.__str
    
    def __repr__(self):
        format_str = '{}({})    # within {} blocks'
        cls = self.__class__.__name__
        if len(self) > 50:
            i = 0
            string = ''
            while len(string) < 50:
                string += self._data[i]
                i += 1
            string = string[:50] + '...'
        else:
            self._to_str()
            string = self.__str
        string = repr(string)
        blocks = len(self._data)
        return format_str.format(cls, string, blocks)
        
    def __add__(self, other):
        new_obj = type(self)(self._data)
        new_obj += other
        return new_obj
    
    def __iadd__(self, other):
        if isinstance(other, str):
            self.append(other)
        elif isinstance(other, ExtendableStr):
            self.extend(other._data)
        elif isinstance(other, Sequence):
            self.extend([str(i) for i in other])
        else:
            self.append(str(other))
        return self
    
    def _to_str(self):
        """Ensure internal string processing completed"""
        
        if self.__formated:
            return
        self.__str = ''.join(self._data)
        self.__length = len(self.__str)
        self._set_cache_status(True, True)
    
    def _set_cache_status(self, str_status: bool = False,
                            len_status: bool = False):
        """Set internal cache status"""
        
        self.__formated = str_status
        self.__measured = len_status
    
    def extend(self, other):
        """Add sequence to end of string
        
        Only processes one level (beware nested sequences)
        Strings added as whole chunks
        Non-sequence arguments converted to string and appended
        """
        
        if isinstance(other, str):
            self.__data.append(other)
        elif isinstance(other, ExtendableStr):
            self.__data.extend(other._data)
        elif isinstance(other, Sequence):
            other = [str(i) for i in other]
            self.__data.extend(other)
        else:
            self.__data.append(str(other))
        self._set_cache_status()
        self._join_if_overflow()
    
    def append(self, other):
        """Add item to end of string
        
        Converts argument to string without traversal
        """
        
        other = str(other)
        self.__data.append(other)
        self._set_cache_status()
        self._join_if_overflow()
    
    def _join_if_overflow(self):
        """Overflow consolidation
        
        Automatically called in append()/extend()
        
        Consolidates to single chunk if chunk count exceeds limit
        """
        
        if self.__overflow:
            if len(self.__data) > self.__overflow:
                self.overflow()
    
    def overflow(self):
        """Consolidate string
        
        Merges all chunks into one
        """
        
        data = ''.join(self.__data)
        self.__data = [data]
        self.__str = data
        self.__length = len(data)
        self._set_cache_status(True, True)

    ## --- Protocol required methods ---
    
    def __len__(self):
        if self.__measured:
            return self.__length
        if self.__formated:
            self.__length = len(self.__str)
        else:
            self.__length = sum(len(block) for block in self.__data)
        self.__measured = True
        return self.__length
    
    @singledispatch
    def __getitem__(self, index):
        raise NotImplementedError('Unsupported type')
    
    @__getitem__.register
    def _(self, index: int) -> str:
        self._to_str()
        data = self.__str[index]
        return data
    
    @__getitem__.register
    def _(self, index: slice) -> Self:
        self._to_str()
        data = self.__str[index]
        return type(self)(data)

    def __contains__(self, value):
        self._to_str()
        value = str(value)
        return value in self.__str
    
    def __iter__(self):
        return (item for block in self._data for item in block)
    
    def __reversed__(self):
        return (item for block in reversed(self._data)
                for item in reversed(block))
    
    def index(self, value):
        self._to_str()
        value = str(value)
        return self.__str.index(value)
    
    def count(self, value):
        self._to_str()
        value = str(value)
        return self.__str.count(value)
