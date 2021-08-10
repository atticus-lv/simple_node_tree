## Simple Node Tree

> This is a very simple node tree which bases on blender UI, which is very suitable for those who want to build their own tree on some purposes.

The update method is based on [rigging_nodes](https://gitlab.com/AquaticNightmare/rigging_nodes) 'runtime system, which cache links and socket value into several dictionary, providing a fast executing speed for the hole tree.

### Nodes

It has some nodes that allow you to do some math computation, including:

+ Input
  + Float input
  + Vector input
+ Math 
  + Boolean math
    + and/or/not
  + Vector math
    + add/subtract/dot/cross/project/normalized/length
  + Function 
    + add/subtract/muitiply/divide
  + Trigonometric
    + sin/cos/tan/asin/acos/atan
  + Conversion
    + to degrees/to radians
  + Comparison
    + greater than/less than/compare/max/min
+ Output
  + Result
+ Utility
  + Float to vector
  + Vector to float
+ Group ( hidden, call by 'Ctrl G')

### Others

This addon also provide a gpu drawing operator that allow you to check the process time of the executing nodes



