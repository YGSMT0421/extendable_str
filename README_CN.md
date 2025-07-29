# extendable_str

提供一个对拼接做出优化的“字符串”类：`extendable_str.ExtendableStr`

`extendable_str.ExtendableStr`是一个对拼接做出特别优化的“字符串”类。它舍弃了一定程度上的访问的性能和`getitem()`、`index()`等需要完整访问字符串的操作的性能。



## 简介

`extendable_str.ExtendableStr`通过维护一个内部字符串列表来保证字符串拼接的效率。会尽可能的进行惰性求值，在需要的时候才进行字符串拼接，并且在拼接后、新的数据加入之间，拼接后的字符串会一直缓存。



下列方法会触发字符串拼接：

* __`__str__()`方法__

* __`overflow()`方法__

* __`__getitem__()`方法__

* __`__contains__()`方法__

* __`index()`方法__

* __`count()`方法__



下列方法会导致缓存失效：

* __`__add__()`和`__iadd__()`方法__

* __`append()`方法__

* __`extend()`方法__



下面是各个方法的详细说明：

* __`__str__()`方法__

    - `__str__()`方法返回内部字符串。

* __`__add__()`__和__`__iadd__()`方法__

    - `__add__()`和`__iadd__()`方法的右操作数应该是其中所有元素都是字符串序列类型。但是实际上它可以传入任意类型的参数，注意：请确保这是你所希望的操作后再使用一个其中所有元素不都是字符串序列的类型。详见`append()`方法和`extend()`方法。

* __`append()`方法__

    - `append(typing.Any) -> None`

    - `append()`方法会将传入的参数直接转化为字符串后加到数据列表的末尾。

* __`extend()`方法__

    - `extend(collections.abc.Sequence) -> None`

    - `extend()`方法会将传入的的序列经过一层（仅经过一层）迭代，将其中的每一项转化为字符串后加入内部数据列表末尾。

    - 当实参是字符串时，会将字符串整体作为一项加入。

    - 当实参是`extendable_str.ExtendableStr`实例时，会将实参内部数据列表加入自己的内部数据列表。

    - 当实参不是序列时，会委托给`append()`方法

* __`overflow()`方法__

    - `overflow() -> None`

    - `overflow()`方法会将所有内部数据拼接为一个字符串后作为新的内部数据列表的第一项。会将其保存为缓存。

* __`__getitem__()`方法__

    - `__getitem__(int) -> str`

    - `__getitem__(slice) -> typing.Self`

    - `__getitem__()`方法返回一个字符串的切片或包含字符串切片的`extendable_str.ExtendableStr`实例

* __`__contains__()`方法__

    - `__contains__(typing.Any) -> bool`

    - `__contains__()`返回实参的字符串形式是否包含在实例所表示的字符串中

* __`__iter__()`方法__

    - `__iter__() -> typing.Iterator[str]`

    - `__iter__()`返回产出实例所表示的字符串形式中每一个字符的迭代器

* __`__reversed__()`方法__

    - `__reversed__() -> typing.Iterator[str]`

    - `__reversed__()`返回反向产出实例所表示的字符串形式中每一个字符的迭代器

* __`index()`方法__

    - `index(typing.Any) -> int`

    - `index()`方法返回实参的字符串形式在实例所表示的字符串中第一次出现的索引。如果提供的实参不在实例所表示的字符串中，抛出`ValueError`。

* __`count()`方法__

    - `count(typing.Any) -> int`

    - `count()`方法返回实参的字符串形式在实例所表示的字符串中出现的次数。



## 超长整合

创建`extendable_str.ExtendableStr`实例时，传入关键字参数`overflow`即可启用超长整合

超长整合限制默认**不启用**



### `overflow: int`

* `overflow`参数是**可选**的

* `overflow`的值必须不小于2。

* 每次使用`__add__()`、`__iadd__()`、`append()`、`extend()`都会触发超长整合限制检测。

* 当实例内部数据列表的长度大于`overflow`所限定的值时，就会调用`overflow()`方法进行整合。



### 手动整合

* 调用`overflow()`方法即可进行手动整合

## 超长整合的继承

- **`inherit: bool = False`**

- `inhert`参数是**可选**的

- 超长整合的继承默认**不启用**

- 当通过一个`inherit`为`True`的`ExtendableStr`实例创建新的实例（不管是通过`getitem()`还是`__init__()`等）时，如果没有指定`overflow`参数，则从原来的实例中继承`overflow`的值

- 如果提供了新实例的`overflow`参数，那么不管原实例的`inherit`是什么，都**以提供的`overflow`为准**

- `inherit`参数的值**不会**被继承

