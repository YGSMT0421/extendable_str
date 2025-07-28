# extendable_str

Provides an optimized "string" class for concatenation: `extendable_str.ExtendableStr`

`extendable_str.ExtendableStr` is a specialized "string" class optimized for concatenation operations. It sacrifices some performance in element access and operations like `getitem()`/`index()` that require full string traversal.



### Introduction

`extendable_str.ExtendableStr` maintains efficiency by keeping an internal list of string fragments. It performs lazy evaluation whenever possible, only concatenating strings when necessary. Once concatenated, the result is cached until new data is added.



Methods that trigger string concatenation:

* `__str__()`

* `overflow()`

* `__getitem__()`

* `__contains__()`

* `index()`

* `count()`



Methods that invalidate the cache:

* `__add__()` and `__iadd__()`

* `append()`

* `extend()`



Detailed method descriptions:

* `__str__()`

  * Returns the internal concatenated string

* `__add__()` and `__iadd__()`

  * The right operand should ideally be a sequence where all elements are strings. In practice, it accepts any type - ensure this matches your intended behavior (see `append()`/`extend()` for details)

* `append()`

  * `append(typing.Any) -> None`

  * Converts the argument to a string and appends it to the internal list

* `extend()`

  * `extend(collections.abc.Sequence) -> None`

  * Iterates through the sequence (single level only), converts each item to a string, and appends them

  * Strings are added as single fragments

  * `ExtendableStr` instances have their fragment lists merged

  * Non-sequence arguments delegate to `append()`

* `overflow()`

  * `overflow() -> None`

  * Joins all fragments into a single string and replaces the internal list with this new fragment

* `__getitem__()`

  * `__getitem__(int) -> str`

  * `__getitem__(slice) -> typing.Self`

  * Returns either a character or a new `ExtendableStr` slice

* `__contains__()`

  * `__contains__(typing.Any) -> bool`

  * Checks if the string representation of the argument exists in the internal string

* `__iter__()`

  * `__iter__() -> typing.Iterator[str]`

  * Returns an iterator yielding each character

* `__reversed__()`

  * `__reversed__() -> typing.Iterator[str]`

  * Returns a reverse character iterator

* `index()`

  * `index(typing.Any) -> int`

  * Returns the first index of the argument's string representation. Raises `ValueError` if not found

* `count()`

  * `count(typing.Any) -> int`

  * Counts occurrences of the argument's string representation



### Overflow Integration

Enable overflow integration by providing the `overflow` keyword argument when creating an `ExtendableStr` instance



#### `overflow: int`

* Must be ≥ 2

* Triggered automatically after `__add__()`, `__iadd__()`, `append()`, or `extend()` operations

* When internal fragment count exceeds the `overflow` value, calls `overflow()` automatically



#### Manual Integration

* Call the `overflow()` method to manually consolidate fragments

