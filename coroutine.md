# [yield](https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement)
  > Yield expressions and statements are only used when defining a [generator](#generator) function, 
  and are only used in the body of the generator function. 
  Using yield in a function definition is sufficient to cause that definition to create
  a generator function instead of a normal function
  
# <span id="generator">[generator](https://docs.python.org/3/glossary.html#term-generator)</span>
  > A function which returns a generator iterator,  
  > suspend firsly, resume and get value by send(value)/next{send(None)}.  
  > **The value of the yield expression after resuming depends on the method which resumed the execution,
    If `__next__()` is used (typically via either a for or the `next()` builtin) then the result is None. 
    Otherwise, if `send()` is used, then the result will be the value passed in to that method** 
    from [yield-expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
  - generator iterator
    > Each yield temporarily suspends processing, remembering the location execution state 
    > (including local variables and pending try-statements). When the generator iterator resumes, 
    > it picks-up where it left-off (in contrast to functions which start fresh on every invocation
  - generator expression
    > An expression that returns an iterator
    
# [asynchronous-generator-functions](https://docs.python.org/3/reference/expressions.html#asynchronous-generator-functions)
  > The presence of a yield expression in a function or method defined using  
    async def further defines the function as a asynchronous generator function
  > managed by asyncio.event_loop()  
  > The expression yield from <expr> is a syntax error when used in an asynchronous generator function
  
# coroutine
  > All of this makes generator functions quite similar to coroutines; 
  they yield multiple times, they have more than one entry point and their execution can be suspended. 
  The only difference is that a generator function cannot control where should the execution continue after it yields; 
  the control is always transferred to the generator’s caller.  
  > that means coroutine = generator + control
