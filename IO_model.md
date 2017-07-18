> http://www.masterraghu.com/subjects/np/introduction/unix_network_programming_v1.3/ch06lev1sec2.html
> http://www.jianshu.com/p/aed6067eeac9
> http://www.jianshu.com/p/486b0965c296

# basic vocabulary
## Blocking
  - waits until function finshed(return)
## non-Blocking
  - return immediately even it has not finished, and query later.
## synchronous
  - waits until function returning(yield)
## asynchronous
  - return immediately even it has not finished， and wake up with callback/event
  - There are many styles of asynchronous interfaces: [tornado_asynchronous](http://www.tornadoweb.org/en/stable/guide/async.html#asynchronous)
    - Callback argument
    - Return a placeholder (Future, Promise, Deferred)
    - Deliver to a queue
    - Callback registry (e.g. POSIX signals)
## memory
  - kenel space
  - user space
## read/write or IO
  - user(application) <---> kenel(buffer) <---> remote
  
# I/O Model
> here we only consider read 
## Blocking and synchronous
  - read until remote send data to kenel ==> Blocking
  - wait until kenel to application ==> synchronous

## non-Blocking and synchronous
  - get error if remote haven't sent data to kenel ==> non-Blocking
  - query next time ==> synchronous
  - else wait until kenel to application ==> synchronous

## Blocking and asynchronous
  - read until remote send data to kenel ==> Blocking
  - when with coroutine/multithread/multiprocess, it go on deal other things  ==> asynchronous
  - get callback after kenel to application ==> asynchronous

## non-Blocking and asynchronous
  - return before remote send data to kenel ==> non-Blocking
  - get callback after kenel to application ==> asynchronous

# I/O Multiplexing Model
  > 1. we call select or poll and block in one of these two system calls, instead of blocking in the actual I/O system call;
  > 2. we can wait for more than one descriptor to be ready, and read just pieces of data ready;
  > 3. in fact, there is a slight disadvantage because using select requires two system calls instead of one. If just few connections, use select/epoll `I/O Multiplexing Model` not ensurely better than `multithread, blocking IO and asynchronous`
  - select, poll, epoll, kqueue
  - register (fd, events, callback) to eventloop
  - select/poll in loop ==> Blocking
  - callback(fd, events) ==> asynchronous
  - wait until kenel to application ==> synchronous
  - modify/unregister (fd, events, callback) to eventloop

# Signal-Driven I/O Model
  - use SIGIO_callback install of event_callback
