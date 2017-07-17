# IO  
- for learning IO  
- async and non-blocking socket, ref: [async-io-and-python](https://blogs.gnome.org/markmc/2013/06/04/async-io-and-python/)
 and [following_comment](https://stackoverflow.com/questions/45095179/how-chained-coroutine-task-get-resumed-by-task-scheduler?noredirect=1#comment77176957_45095179) ==>
**about `asyncio`, my understanding is that `NonBlcoking` is not blocking on `read()/recv()` which waiting remote `recv/read` and `read/write` from `buff` which `send/recv` remote backgroud, but without `async` you still have to wait for `read()/recv()` done to do next;  about `async` this [asynchronous](http://www.tornadoweb.org/en/stable/guide/async.html#asynchronous) is a good explanation, here considered to be `Future` and `epoll/kqueue/select`, callback if done else do other things.**


# task  
- status to msg

|status|msg|
|------|---|
-999|unhandle error|
-990|retry required|
-980|retry optional|
-970|retry later|
-900~-950|unrepeatful|
-601~-899|reserved|
-100~-600|http code|
-1~-200|errno|
0|succ|
1-100|init|
100-800|inprocess|
800-900|callback|
900-999|reserved|

- operate
  - RESTful API

- scan task distributable
  - periodically task add `msg` to `queue` unless `No msg`, to ensure only one `msg` 
  several workers watch this `queue` and custom it with `ack required` (server-server)
  - one down one up (server-standby)
  
