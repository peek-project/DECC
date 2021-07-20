
## Language Reference
##### Introduction

Decimal script 1.2 is the script programming language. You can print out "Hello, World!" as follows.

```
write("Hello, World!\n");
```

##### Comment

In decimal script, comment is defined as follows.

```
#comment message
```

##### Data types

Decimal script has the following data type.

* number
* string
* array

```
123456789.123456788; #number
"Hello, World!";     #string
{1, 2, 3, 4, 5, 6};  #array
```

In decimal script, any number of operations can use a fixed decimal point, and a string can use either a "string" or a 'string'.

true and false are automatically converted to 1 and 0.

The string supports the following control characters: \t \n \" \' \\\\

##### Operators

In decimal script, operator priorities are as follows.

1. ( )
2. \* / % ^
3. \+ -
4. == != >= <= > <
5. & | !
6. = += -= *= /= %= ^=

##### Variables

A variable can be put in a value by using an operator. In decimal script, variables do not need to be declared first.

```
Number = 123;
String = "hello";
Array = {1, 2, 3};
```

Array variables can also refer to indexes as follows.

```
Array = {1, 2, 3};
Array[0];
```

##### Control statements

Decimal script in, you can write such letters as follows.

```
if(expression) command;
else if(expression) command;
else command;
```

Next, while, until, for loop commands supported.

```
while(expression) command;

until(expression) command;

for(initialization; condition; afterthought) command;
```

You can create blocks of commands as follows.

```
{ command1; command2; ... }
```

##### Functions

In decimal script, a function can be defined as follows.

```
define(factor1, factor2, ...) command;
```

Returns can be made as follows.

```
return(value);
```

The call of the function is as follows.

```
function(factor1, factor2, ...);
```

Calls to a function can also be made within an expressions.

```
a = 10 + num(10);
```

##### Default function

* quit(exit code) end program

* write(text) write text

* read() read and return text

* fopen(file name, open type) open file and return file code

* fclose(file code) close file

* fwrite(file code, text) write text for file

* fread(file code) read from file and return

* python(code) exec python code

* exec(code) exec decimal script code

* system(command) exec system command

* num(data) convert data to text

* str(data) convert data to text

* arr(len) create array with length len

* len(array) return len of arrray

* chr(ascii) ascii code to char

* ord(char) char to ascii code

##### Examples

Decimal script code to obtain Fibonacci sequence.
```
#define function
define F(n) {
  if(mem[n]) return(mem[n]);
  if(n <= 1) return(n);
  else {
    mem[n] = F(n - 1) + F(n - 2);
    return(mem[n]);
  }
}

#main
write("n = ");
N = num(read());
mem = arr(N + 1);
result = F(N);
write("F(n) = " + str(result) + '\n');
```
