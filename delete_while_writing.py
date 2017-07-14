with open('t','w') as fp:
    fp.write('fsdfds')
    fp.flush()
    try:
        while True:
            import time
            time.sleep(3)
            fp.write('f\n')
            fp.flush()
    except KeyboardInterrupt:
        # No error, but can't save file
        # maybe shutil -XXX-> better not, waste source!
        fp.flush()
# FileNotFoundError: [Errno 2] No such file or directory: 't' -> 't1'
os.link('t','t1')
