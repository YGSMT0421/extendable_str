# extendable_str

提供一个对拼接做出优化的“字符串”类：`extendable_str.ExtendableStr`

`extendable_str.ExtendableStr`是一个对拼接做出特别优化的“字符串”类。它舍弃了一定程度上的访问的性能和`getitem()`、`index()`等需要完整访问字符串的性能。



# extendable_str

Provides an optimized "string" class for concatenation: `extendable_str.ExtendableStr`

`extendable_str.ExtendableStr` is a specialized "string" class optimized for concatenation operations. It sacrifices some performance in element access and operations like `getitem()`/`index()` that require full string traversal.



查阅完整简体中文版README请查阅`README_CN.md`

For the full English README, please refer to `README_EN.md`