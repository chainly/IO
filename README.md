# IO  
- for learning IO  
- async and non-blocking socket, ref: [async-io-and-python](https://blogs.gnome.org/markmc/2013/06/04/async-io-and-python/)
 and [following_comment](https://stackoverflow.com/questions/45095179/how-chained-coroutine-task-get-resumed-by-task-scheduler?noredirect=1#comment77176957_45095179) ==>
**about `asyncio`, my understanding is that `NonBlcoking` is not blocking on `read()/recv()` which waiting remote `recv/read` and `read/write` from `buff` which `send/recv` remote backgroud, but without `async` you still have to wait for `read()/recv()` done to do next;  about `async` this [asynchronous](http://www.tornadoweb.org/en/stable/guide/async.html#asynchronous) is a good explanation, here considered to be `Future` and `epoll/kqueue/select`, callback if done else do other things.**
- more see [IO_model.md](./IO_model.md)
- about `generator/coroutine` ,see [coroutine](./coroutine.md)

# pid, gid, sid
  > http://chimera.labs.oreilly.com/books/1230000000393/ch12.html#_launching_a_daemon_process_on_unix
  > https://stackoverflow.com/questions/25701333/os-setsid-operation-not-permitted/35444688#35444688
  > http://www.cnblogs.com/forstudy/archive/2012/04/03/2427683.html
  1. pid = os.getpid()
  2. ppid = os.getppid()
  3. gid = os.getpgid(os.getpid())
  4. sid = os.getsid(os.getpid())
  5. gid2 = os.setpgid
  6. sid <-- gid <--- (ppid <- pid)
  7. os.setsid() # create new sid2 (raise if gid == pid # gid leader) and sid2.gid == pid (new sid's gid's leader)
  

# pool
  > https://github.com/studio-ousia/gsocketpool/blob/master/gsocketpool/pool.py
  
  1. _pool = _inuse = []; max = max; max_timeout/retry
  2. len, len(_pool + _inuse)
  3. new, len()?max : conn=create_conn; _pool.append(conn), raise/wait
  4. valid, conn.valid?
  5. get, for conn in _pool, valid？move_to_inuse return,continue; else, new
  6. with contextlib finally, move_to_pool |& valid
  7. close, do_nothing/conn.close

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
  - query add cache && cache_time in repsonse

- scan task distributable
  - periodically task add `msg` to `queue` unless `No msg`, to ensure only one `msg` 
  several workers watch this `queue` and custom it with `ack required` (server-server)
  - one down one up (server-standby)
  - `Beat`: `select_for_update` and `is_locked` as `table_column` add it to `Worker`(for `routing` and `separated`); `Worker`: do_job (preferred)
  
# log
 - format: 'short desc, %detail_info: %key'
 - debug: for traceback
 - warn: for operating failed but not very important
 - info: for operating succ
 - error: for operating failed but important
 - critical: for sytemExit, system error, logic error or unhandle error that must exit.
