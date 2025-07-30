"""extendable_str module, provides an ExtendStr class optimized for frequent appending

The module contains one class: ExtendableStr

English version is translated by DeepSeek
"""

from collections.abc import Sequence
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
    
    8. inherit=True enables overflow inheritance to new instances
    Regardless of creation method (getitem() or __init__()), when creating new instances 
    from an ExtendableStr instance with inherit=True, the new instance inherits overflow 
    unless overflow is explicitly provided
    >>> es = ExtendableStr('Kokomi', overflow=5, inherit=True)
    >>> es.extend(range(5))
    >>> es    # Overflow limit applied
    ExtendableStr('Kokomi01234')    # within 1 blocks
    >>> tmp = ExtendableStr(es)    # Inherits overflow from es
    >>> tmp
    ExtendableStr('Kokomi01234')    # within 1 blocks
    >>> tmp.extend(range(5))
    >>> tmp    # Confirms overflow inheritance
    ExtendableStr('Kokomi0123401234')    # within 1 blocks
    >>> tmp = ExtendableStr(es, overflow=10)    # Explicit overflow
    >>> tmp.extend(range(5))
    >>> tmp    # No inheritance (explicit overflow used)
    ExtendableStr('Kokomi0123401234')    # within 6 blocks
    >>> tmp.extend(range(5))
    >>> tmp    # Overflow limit triggered
    ExtendableStr('Kokomi012340123401234')    # within 1 blocks
    
    Manual consolidation:
    -----
    
    9. Manually consolidate instance
    >>> es = ExtendableStr()    # Create new instance
    >>> es.extend(range(5))
    >>> es
    ExtendableStr('01234')    # within 5 blocks
    >>> es.overflow()
    >>> es
    ExtendableStr('01234')    # within 1 blocks
    
    Sequence methods:
    -----
    
    10. len() returns string length without concatenation
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
    
    11. getitem() returns specific string items
    Integer index returns single character
    Slice returns ExtendableStr with result
    >>> es = ExtendableStr()    # Create new instance
    >>> es.append('Sangonomiya Kokomi')
    >>> es[0]
    'S'
    >>> es[-6:]
    ExtendableStr('Kokomi')    # within 1 blocks
    
    12. Other methods
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
                 overflow: int | None = None,
                 inherit: bool = False):
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
            inherit: Boolean type
                Enable overflow inheritance. When creating new instances from an ExtendableStr instance 
                with inherit=True, new instance inherits overflow unless overflow is explicitly provided
                Note: Explicit overflow parameter takes precedence over inheritance
                inherit itself is not inherited
                Default: False (inheritance disabled)
        """
        if seq is None:
            self.__data = []
            self.__length = 0
        else:
            if isinstance(seq, str):
                self.__data = [seq]
                self.__length = len(seq)
            elif isinstance(seq, ExtendableStr):
                self.__data = seq._data[:]
                self.__length = len(seq)
            elif isinstance(seq, Sequence):
                self.__data = [str(i) for i in seq]
                self.__length = sum((len(s) for s in self.__data))
            else:
                self.__data = [str(seq)]
                self.__length = len(self.__data[0])
        self.__str = ''
        self.__formated = False
        if overflow is None:
            if isinstance(seq, ExtendableStr) and seq._inherit:
                self._overflow = seq._overflow
            else:
                self._overflow = 0
        elif overflow < 2:    # Must be greater than 1
            raise ValueError(f'Overflow limit must be >1, got {overflow}')
        else:
            self._overflow = overflow
        self._inherit = inherit
    
    @property
    def _data(self) -> list[str]:
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
        
    def __add__(self, other) -> Self:
        overflow = self._overflow if self._inherit else None
        new_obj = type(self)(self._data, overflow=overflow, inherit=self._inherit)
        new_obj += other
        return new_obj
    
    def __iadd__(self, other) -> Self:
        if isinstance(other, str):
            self.append(other)
        elif isinstance(other, ExtendableStr):
            self.extend(other._data)
        elif isinstance(other, Sequence):
            self.extend([str(i) for i in other])
        else:
            self.append(str(other))
        return self
    
    def _to_str(self) -> None:
        """Ensure internal string processing completed"""
        
        if self.__formated:
            return
        self.__str = ''.join(self._data)
        self.__length = len(self.__str)
        self.__formated = True
    
    def extend(self, other: Sequence) -> Self:
        """Add sequence to end of string
        
        Only processes one level (beware nested sequences)
        Strings added as whole chunks
        Non-sequence arguments converted to string and appended
        """
        
        if isinstance(other, str):
            self.__data.append(other)
            self.__length += len(other)
        elif isinstance(other, ExtendableStr):
            self.__data.extend(other._data)
            self.__length += len(other)
        elif isinstance(other, Sequence):
            other = [str(i) for i in other]
            length = sum((len(s) for s in other))
            self.__data.extend(other)
            self.__length += length
        else:
            self.__data.append(str(other))
        self.__formated = False
        self._join_if_overflow()
    
    def append(self, other: Any) -> None:
        """Add item to end of string
        
        Converts argument to string without traversal
        """
        
        other = str(other)
        self.__data.append(other)
        self.__length += len(other)
        self.__formated = False
        self._join_if_overflow()
    
    def _join_if_overflow(self) -> None:
        """Overflow consolidation
        
        Automatically called in append()/extend()
        
        Consolidates to single chunk if chunk count exceeds limit
        """
        
        if self._overflow:
            if len(self.__data) > self._overflow:
                self.overflow()
    
    def overflow(self) -> None:
        """Consolidate string
        
        Merges all chunks into one
        """
        
        data = ''.join(self.__data)
        self.__data = [data]
        self.__str = data
        self.__length = len(data)
        self.__formated = True

    ## --- Protocol required methods ---
    
    def __len__(self):
        return self.__length
    
    def __getitem__(self, index):
        if isinstance(index, int):
            self._to_str()
            return self.__str[index]
        elif isinstance(index, slice):
            self._to_str()
            data = self.__str[index]
            overflow = self._overflow if self._inherit else None
            new = type(self)(data, overflow=overflow, inherit=self._inherit)
            return new
        else:
            raise NotImplementedError(f"Unsupported type: {type(index)}")
    
    def __contains__(self, value):
        self._to_str()
        value = str(value)
        return value in self.__str
    
    def __iter__(self):
        return (item for block in self._data for item in block)
    
    def __reversed__(self):
        return (item for block in reversed(self._data)
                for item in reversed(block))
    
    def index(self, value: Any) -> int:
        self._to_str()
        value = str(value)
        return self.__str.index(value)
    
    def count(self, value: Any) -> int:
        self._to_str()
        value = str(value)
        return self.__str.count(value)
