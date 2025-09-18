import threading, time, random
from queue import Queue

class Proc(threading.Thread):
    def __init__(self, pid, inboxes):
        super().__init__(); self.pid,self.inboxes=pid,inboxes; self.inbox=inboxes[pid]; self.N=len(inboxes)

    def send(self,to,msg): self.inboxes[to].put(msg)

    def run(self):
        while True:
            token=self.inbox.get()
            if token is None: break
            if random.random()<0.5:  # decide to enter CS
                print(f"P{self.pid} ENTER CS"); time.sleep(0.3); print(f"P{self.pid} EXIT CS")
            self.send((self.pid+1)%self.N,token)

if __name__=="__main__":
    N=3
    inboxes=[Queue() for _ in range(N)]
    procs=[Proc(i,inboxes) for i in range(N)]
    [p.start() for p in procs]
    inboxes[0].put("TOKEN")   # start with one token
    time.sleep(5)             # let them run
    [q.put(None) for q in inboxes]   # stop
    [p.join() for p in procs]
    print("Token Ring Finished.")
