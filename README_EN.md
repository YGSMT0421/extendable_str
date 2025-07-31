# extendable_str

Provides an optimized "string" class for concatenation: `extendable_str.ExtendableStr`

`extendable_str.ExtendableStr` is a specialized "string" class optimized for concatenation operations. It sacrifices some performance in element access and operations like `getitem()`/`index()` that require full string traversal.

## Introduction

`extendable_str.ExtendableStr` maintains efficiency by keeping an internal list of string fragments. It performs lazy evaluation whenever possible, only concatenating strings when necessary. Once concatenated, the result is cached until new data is added.

Methods that trigger string concatenation:

* __`__str__()`__

* __`overflow()`__

* __`__getitem__()`__

* __`__contains__()`__

* __`index()`__

* __`count()`__



Methods that invalidate the cache:

* __`__add__()`__ and __`__iadd__()`__

* __`append()`__

* __`extend()`__



Detailed method descriptions:

* __`__str__()`__

  * Returns the internal concatenated string

* __`__add__()`__ and __`__iadd__()`__

  * The right operand should ideally be a sequence where all elements are strings. In practice, it accepts any type - ensure this matches your intended behavior (see `append()`/`extend()` for details)

* __`append()`__

  * `append(typing.Any) -> None`

  * Converts the argument to a string and appends it to the internal list

* __`extend()`__

  * `extend(collections.abc.Sequence) -> None`

  * Iterates through the sequence (single level only), converts each item to a string, and appends them

  * Strings are added as single fragments

  * `ExtendableStr` instances have their fragment lists merged

  * Non-sequence arguments delegate to `append()`

* __`overflow()`__

  * `overflow() -> None`

  * Joins all fragments into a single string and replaces the internal list with this new fragment

* __`__getitem__()`__

  * `__getitem__(int) -> str`

  * `__getitem__(slice) -> typing.Self`

  * Returns either a character or a new `ExtendableStr` slice

* __`__contains__()`__

  * `__contains__(typing.Any) -> bool`

  * Checks if the string representation of the argument exists in the internal string

* __`__iter__()`__

  * `__iter__() -> typing.Iterator[str]`

  * Returns an iterator yielding each character

* __`__reversed__()`__

  * `__reversed__() -> typing.Iterator[str]`

  * Returns a reverse character iterator

* __`index()`__

  * `index(typing.Any) -> int`

  * Returns the first index of the argument's string representation. Raises `ValueError` if not found

* __`count()`__

  * `count(typing.Any) -> int`

  * Counts occurrences of the argument's string representation


## Overflow Integration

Enable overflow integration by providing the `overflow` keyword argument when creating an `ExtendableStr` instance.

Overflow integration is **disabled** by default.


### `overflow: int`

* `overflow` parameter is **optional**

* Value must be ≥ 2 (raises `ValueError` otherwise)

* Triggered automatically after `__add__()`, `__iadd__()`, `append()`, or `extend()` operations

* When internal fragment count exceeds the `overflow` value, calls `overflow()` automatically


### Inheritance of overflow

* **`inherit: bool = False`**

* `inherit` parameter is **optional**

* Overflow inheritance is **disabled** by default

* When creating new instances (via `__init__` or slicing) from an `ExtendableStr` instance with `inherit=True`, the new instance will inherit the `overflow` value from the original instance if no `overflow` parameter is provided

* Explicitly providing `overflow` during creation takes precedence over inheritance

* The `inherit` parameter value is **not** inherited by new instances


### Manual Integration

* Call the `overflow()` method to manually consolidate fragments