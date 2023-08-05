from typing import Union, final

from pygame.event import Event

def get_ticks() -> int: ...
def wait(milliseconds: int) -> int: ...
def delay(milliseconds: int) -> int: ...
def set_timer(event: Union[int, Event], millis: int, loops: int = 0) -> None: ...
@final
class Clock:
    def tick(self, framerate: float = 0) -> int: ...
    def tick_busy_loop(self, framerate: float = 0) -> int: ...
    def get_time(self) -> int: ...
    def get_rawtime(self) -> int: ...
    def get_fps(self) -> float: ...
