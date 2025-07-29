"""extendable_str模块，提供一个对常追加优化的ExtendStr类

模块包含了一个类：ExtendStr
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
    """需求常追加，少读取的字符串
    
    ExtendableStr继承自collections.abc.Sequence类
    
    创建新的实例：
    -------
    
    1. 创建空的实例
    >>> es = ExtendableStr()
    
    2. 从初始字符串新建
    >>> es = ExtendableStr('Sangonomiya Kokomi')
    
    3. 从初始序列创建（会将序列中所有元素转换为字符串）
    >>> es = ExtendableStr([0, 'a', range(5)])
    >>> es = ExtendableStr((0, 'a', range(5)))
    >>> es = ExtendableStr(range(5))
    
    4. 从其他类型创建（会将其转换为字符串）
    >>> es = ExtendableStr(0)
    
    添加块：
    ----
    
    5. 添加单个块
    注意：若需要添加一个序列（除了字符串）请使用extend(seq)方法！
    >>> es = ExtendableStr()    #创建新的实例
    >>> es.append('abc')
    >>> print(es)
    abc
    >>> es.append(0)
    >>> print(es)
    abc0
    
    6. 添加多个块（添加序列）
    >>> es = ExtendableStr()    #创建新的实例
    >>> tmp = ExtendableStr(list('tmp'))
    >>> es.extend([1, 2, 3])
    >>> es
    ExtendableStr('123')    # within 3 blocks
    >>> es + tmp    # ExtendableStr实例会将其中的每个块分别加入
    ExtendableStr('123tmp')    # within 6 blocks
    >>> es.extend(range(5))
    >>> es
    ExtendableStr('12301234')    # within 8 blocks
    >>> es.extend('abc')    # 字符串会作为一个整体加入
    >>> es
    ExtendableStr('12301234abc')    # within 9 blocks
    
    超长整合限制：
    -------
    
    当块数大于给定的限制时，会将所有块合并为一个字符串并替代原有块作为新的块
    超长整合限制默认不启用。如果需要启用，在初始化实例时为overflow参数传入一个不小于2的整数。如果值小于2，抛出ValueError。
    
    7. 超长整合限制可以在一定程度上减小过多块导致的性能浪费
    >>> es = ExtendableStr(overflow=5)    # 创建新的实例，限制块数最大为5
    >>> es.append('Kokomi')
    >>> es
    ExtendableStr('Kokomi')    # within 1 blocks
    >>> es.extend([1, 2, 3])
    >>> es
    ExtendableStr('Kokomi123')    # within 4 blocks
    >>> es.extend(range(5))
    >>> # 此时已经触发超长整合限制，将所有块整合成一个块
    >>> es
    ExtendableStr('Kokomi12301234')    # within 1 blocks
    
    8. inherit为True可以让以此为基础的实例继承overflow
    不管是通过getitem()还是直接传入__init__()，只要是通过inherit为True的ExtendableStr实例创建的新实例，
    都会继承overflow
    >>> es = ExtendableStr('Kokomi', overflow=5, inherit=True)    # 创建新的实例，并启用继承
    >>> es.extend(range(5))
    >>> es    # 确认超长整合限制已经启用
    ExtendableStr('Kokomi01234')    # within 1 blocks
    >>> tmp = ExtendableStr(es)    # 不指定overflow，将从es中继承
    >>> tmp    # 确认数据继承
    ExtendableStr('Kokomi01234')    # within 1 blocks
    >>> tmp.extend(range(5))
    >>> tmp    # 确认overflow也已继承
    ExtendableStr('Kokomi0123401234')    # within 1 blocks
    >>> tmp = ExtendableStr(es, overflow=10)    # 指定overflow
    >>> tmp.extend(range(5))
    >>> tmp    # 未继承overflow
    ExtendableStr('Kokomi0123401234')    # within 6 blocks
    >>> tmp.extend(range(5))
    >>> tmp    # 触发超长整合限制
    ExtendableStr('Kokomi012340123401234')    # within 1 blocks
    
    手动整合：
    -----
    
    8. 手动对实例进行整合
    >>> es = ExtendableStr()    # 创建新的实例
    >>> es.extend(range(5))
    >>> es
    ExtendableStr('01234')    # within 5 blocks
    >>> es.overflow()
    >>> es
    ExtendableStr('01234')    # within 1 blocks
    
    序列方法：
    -----
    
    9. len()方法会返回其中字符串的长度
    len()方法不会对字符串进行操作
    >>> es = ExtendableStr()    # 创建新的实例
    >>> es.append('Sangonomiya')
    >>> # 字符串仍然没有被拼接过
    >>> len(es)
    11
    >>> # 在此之间内部没有进行任何操作
    >>> es.append(' Kokomi')
    >>> len(es)
    18
    >>> # 在此之前字符串没有被拼接过
    >>> print(es)    # 字符串第一次被拼接
    Sangonomiya Kokomi
    
    10. getitem()方法返回字符串的特定项
    整数索引会返回单个字符串
    slice实例会返回包含结果的ExtendableStr实例
    >>> es = ExtendableStr()    # 创建新的实例
    >>> es.append('Sangonomiya Kokomi')
    >>> es[0]
    'S'
    >>> es[-6:]
    ExtendableStr('Kokomi')    # within 1 blocks
    
    11. 其余方法
    >>> es = ExtendableStr()    # 创建新的实例
    >>> es.append('Sangonomiya Kokomi')
    
    in运算符（会将左运算符自动转换为字符串）
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
        参数：
            seq: 序列类型
                序列会经过一层迭代将其中所有项转换为字符串后作为实例的初始内容
                可以为空。默认行为是创建一个空的实例
                如果传入的不是一个序列，那么会将它转换为字符串后作为初始的块。不建议这么做，除非你确定这是你希望的行为
            overflow: 整数类型
                超长整合限制。如果提供了，当块数大于这个值时会触发超长整合
                值必须不小于2，否则会抛出ValueError
                可以为空。默认行为是不启用此功能
                即便为空，你也可以主动调用overflow()方法进行整合
            inherit：布尔类型
                是否继承超长整合限制。如果提供了，当**创建新的实例**时传入inherit为True的ExtendableStr实例时，
                如果未提供overflow，则自动将overflow设为提供的实例的overflow
                注意：overflow的优先级大于inherit。这意味着如果传入了overflow，
                即便传入的ExtendableStr实例的inherit为True, 也以传入的overflow为准
                inherit不会被继承
                可以为空。默认行为是不启用此功能
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
        elif overflow < 2:    # 长度必须大于1
            raise ValueError(f'超长整合限制必须大于1，但是提供的是{overflow}')
        else:
            self._overflow = overflow
        self._inherit = inherit
    
    @property
    def _data(self) -> list[str]:
        """返回内部状态，注意用户不应该调用此方法"""
        
        return self.__data
    
    def __str__(self):
        """返回实例内部的字符串"""
        
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
        new_obj = type(self)(self._data, overflow=overflow)
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
        """确保内部字符串处理完成"""
        
        if self.__formated:
            return
        self.__str = ''.join(self._data)
        self.__length = len(self.__str)
        self.__formated = True
    
    def extend(self, other: Sequence) -> Self:
        """Add sequence to end of string
        
        只会遍历一层，在传入嵌套序列时请确保这是否符合预期
        字符串会作为一个整体添加到末尾
        如果提供的实参不是序列，那么会直接转化为字符串后使用append()方法添加到末尾
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
        """在实例所表示的字符串末尾添加一项
        
        会将提供的实参直接转换为字符串后添加，不会进行任何遍历
        """
        
        other = str(other)
        self.__data.append(other)
        self.__length += len(other)
        self.__formated = False
        self._join_if_overflow()
    
    def _join_if_overflow(self) -> None:
        """超长整合限制
        
        在append()方法和extend()方法中自动调用
        
        检测到内部块数多于指定数量（如果指定了）后将字符串整合为一个块
        """
        
        if self._overflow:
            if len(self.__data) > self._overflow:
                self.overflow()
    
    def overflow(self) -> None:
        """整合字符串
        
        将所有块整合为一个块
        """
        
        data = ''.join(self.__data)
        self.__data = [data]
        self.__str = data
        self.__length = len(data)
        self.__formated = True

    ## --- 协议所需方法 ---
    
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
            new = type(self)(data, overflow=overflow)
            return new
        else:
            raise NotImplementedError(f"不支持的类型: {type(index)}")
    
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
