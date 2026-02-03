import time
import threading
class Clock:
    def __init__(self, interval=0.001):
        self.now = time.time()
        self._running = True
        self._interval = interval
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            self.now = time.time()
            time.sleep(self._interval)

    def stop(self):
        self._running = False
        self._thread.join()


clock = Clock()


class timer:
    def __init__(self):
        self.clock = clock
        self.elapse = time.time()
        self.pause_time = -1

    def pause(self):
        self.pause_time = self.elapsed()

    def resume(self):
        self.set(self.pause_time)
        self.pause_time = -1

    def set(self, new_time):
        self.elapse = time.time() - self._seconds(new_time)

    def restart(self):
        self.elapse = time.time()
        self.pause_time = -1

    def elapsed(self):
        if self.pause_time != -1:
            return self.pause_time
        else:
            return self._ms(self.clock.now - self.elapse)

    def _ms(self, t):
        return int(t * 1000)

    def _seconds(self, milliseconds):
        return milliseconds / 1000
