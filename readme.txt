alright.

so, u decided to open dis.

Roight. Well, you need to run this first:

pip3 install sly

Das it. Then, ur dun.

To run a file, do 'py -3 calc_cli.py your_script.cum'

===

CLI USAGE:

# Interpret a file
py -3 calc_cli.py your_script.cum

# Compile a file
py -3 calc_cli.py your_script.cum --compile --output output_cum

# Compile a file to readable assembly (you can also add --output to redirect)
py -3 calc_cli.py your_script.cum --compile-asm

# Interpret a bytecode file
py -3 calc_cli.py bytecode_cum --bytecode

===

The language is pretty simple.

Expressions: Math, bitch.
print(1 + 2 * 4 / (-5 + 8 * 3))

Strings; Yes.
print("Hello " + "world!")

Functions; heeel yeah.

Cumulative Upgrading Multiplexer (CUM) lang has a very extensive and thorough standard library feature over (at least) 2 functions.
These functions are the language's main feature and can be strung together to make anything.

For example, finding length of a 2d line (Pythagoreas' theorum):

```cum

x1 = 2;
y1 = 5;
x2 = 10;
y2 = 12;

dist = sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1));
print(dist);

```

Output is: 10.63014581273465
Very accurate, as you see.

The standard library (LONG):
 * print - Prints shit.
 * sqrt - Square root.

Whew! That was a lot, wasn't it?

Assigning variables is simply:

```cum
x = 123
```

That's all. No multi assignment. Each assignment takes it's own line.

Finally, each statement is separated by a semicolon.