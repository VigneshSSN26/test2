import threading, time, random
from queue import Queue, Empty

class Proc(threading.Thread):
    def __init__(self, pid, inboxes):
        super().__init__(); self.pid, self.inboxes = pid, inboxes
        self.N, self.clock, self.req_time = len(inboxes), 0, None
        self.requesting, self.deferred, self.replies = False, set(), set()
        self.inbox = inboxes[pid]

    def send(self, to, msg): self.inboxes[to].put((self.pid, msg))
    def broadcast(self, msg): [self.send(i, msg) for i in range(self.N) if i!=self.pid]

    def handle(self, sender, msg):
        typ, val = msg
        if typ=="REQ":
            self.clock=max(self.clock,val)+1
            if (not self.requesting) or ((val,sender)<(self.req_time,self.pid)):
                self.send(sender,("REPLY",None))
            else: self.deferred.add(sender)
        elif typ=="REPLY": self.replies.add(sender)

    def run(self):
        for _ in range(2):
            time.sleep(random.random()+0.3)
            print(f"P{self.pid} requests CS")
            self.requesting, self.clock = True, self.clock+1
            self.req_time, self.replies = self.clock, set()
            self.broadcast(("REQ", self.req_time))

            while len(self.replies)<self.N-1:
                try: s,m=self.inbox.get(timeout=0.3); self.handle(s,m)
                except Empty: pass

            print(f"P{self.pid} ENTER CS"); time.sleep(0.4); print(f"P{self.pid} EXIT CS")
            self.requesting=False
            [self.send(p,("REPLY",None)) for p in list(self.deferred)]; self.deferred.clear()

if __name__=="__main__":
    N=3
    inboxes=[Queue() for _ in range(N)]
    procs=[Proc(i,inboxes) for i in range(N)]
    [p.start() for p in procs]; [p.join() for p in procs]
    print("Ricart–Agrawala Finished.")
