# IO  
- for learning IO  


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
  - several workers watch this `queue` and custom it with `ack required`
  
