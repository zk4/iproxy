#!/Users/zk/anaconda3/bin/python
#coding: utf-8

import sys
import subprocess
import iproxy.iproxy as i
from datetime import datetime
if __name__ == "__main__":
    print(sys.argv)

    ip = sys.argv[3]
    port =sys.argv[4]
    
    ret = i.check(f"socks5h://{ip}:{port}")
    ret =False
    now = datetime. now()
    current_time = now. strftime("%H:%M:%S")

    if ret:
        with open("/Users/zk/git/pythonPrj/iproxy/check.log","w") as f:
            f.write(f"{current_time}:  {ip}:{port}\n")
        sys.exit(0)
    else:
        with open("/Users/zk/git/pythonPrj/iproxy/check.log","w") as f:
            normal = subprocess.run(["ls"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True,
                        text=True)
            f.write(normal.stdout)

            sys.exit(1)
            print("hello")

    
