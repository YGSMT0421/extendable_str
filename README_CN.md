# extendable_str

提供一个对拼接做出优化的“字符串”类：`extendable_str.ExtendableStr`

`extendable_str.ExtendableStr`是一个对拼接做出特别优化的“字符串”类。它舍弃了一定程度上的访问的性能和`getitem()`、`index()`等需要完整访问字符串的性能。



### 简介

`extendable_str.ExtendableStr`通过维护一个内部字符串列表来保证字符串拼接的效率。会尽可能的进行惰性求值，在需要的时候才进行字符串拼接，并且在拼接后、新的数据加入之间，拼接后的字符串会一直缓存。



下列方法会触发字符串拼接：

    * `__str__()`方法

    * `overflow()`方法

    * `__getitem__()`方法

    * `__contains__()`方法

    * `index()`方法

    * `count()`方法



下列方法会导致缓存失效：

    * `__add__()`和`__iadd__()`方法

    * `append()`方法

    * `extend()`方法



下面是各个方法的详细说明：

    * `__str__()`方法

        * `__str__()`方法返回内部字符串。

    * `__add__()`和`__iadd__()`方法

        * `__add__()`和`__iadd__()`方法的右操作数应该是其中所有元素都是字符串序列类型。但是实际上它可以传入任意类型的参数，注意：请确保这是你所希望的操作后再使用一个其中所有元素不都是字符串序列的类型。详见`append()`方法和`extend()`方法。

    * `append()`方法

        * `append(typing.Any) -> None`

        * `append()`方法会将传入的参数直接转化为字符串后加到数据列表的末尾。

    * `extend()`方法

        * `extend(collections.abc.Sequence) -> None`

        * `extend()`方法会将传入的的序列经过一层（仅经过一层）迭代，将其中的每一项转化为字符串后加入内部数据列表末尾。

        * 当实参是字符串时，会将字符串整体作为一项加入。

        * 当实参是`extendable_str.ExtendableStr`实例时，会将实参内部数据列表加入自己的内部数据列表。

        * 当实参不是序列时，会委托给`append()`方法

    * `overflow()`方法

        * `overflow() -> None`

        * `overflow()`方法会将所有内部数据拼接为一个字符串后作为新的内部数据列表的第一项。会将其保存为缓存。

    * `__getitem__()`方法

        * `__getitem__(int) -> str`

        * `__getitem__(slice) -> typing.Self`

        * `__getitem__()`方法返回一个字符串的切片或包含字符串切片的`extendable_str.ExtendableStr`实例

    * `__contains__()`方法

        * `__contains__(typing.Any) -> bool`

        * `__contains__()`返回实参的字符串形式是否包含在实例所表示的字符串中

    * `__iter__()`方法

        * `__iter__() -> typing.Iterator[str]`

        * `__iter__()`返回产出实例所表示的字符串形式中每一个字符的迭代器

    * `__reversed__()`方法

        * `__reversed__() -> typing.Iterator[str]`

        * `__reversed__()`返回反向产出实例所表示的字符串形式中每一个字符的迭代器

    * `index()`方法

        * `index(typing.Any) -> int`

        * `index()`方法返回实参的字符串形式在实例所表示的字符串中第一次出现的索引。如果提供的实参不在实例所表示的字符串中，抛出`ValueError`。

    * `count()`方法

        * `count(typing.Any) -> int`

        * `count()`方法返回实参的字符串形式在实例所表示的字符串中出现的次数。



### 超长整合

创建`extendable_str.ExtendableStr`实例时，传入关键字参数`overflow`即可启用超长整合



#### `overflow: int`

    * `overflow`的值必须不小于2。

    * 每次使用`__add__()`、`__iadd__()`、`append()`、`extend()`都会触发超长整合限制检测。

    * 当实例内部数据列表的长度大于`overflow`所限定的值时，就会调用`overflow()`方法进行整合。



#### 手动整合

    * 调用`overflow()`方法即可进行手动整合

