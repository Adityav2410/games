import time
import threading
from .blocks import Block
from .obstacles_and_players import ObstacleManager, Player
from ui import display_blocks_and_get_user_input


class Engine():
    def __init__(self, timer_frequency_ms, ui_title, arena_w, arena_h, player_step_size):
        self._timer_frequency_ms = timer_frequency_ms
        self._ui_title = ui_title
        self._player_step_size = player_step_size
        self._arena = Block.from_width_height(arena_w, arena_h)
        self._obstacle_manager = ObstacleManager()
        self._player = Player()
        self._timer = Timer(self, self._timer_frequency_ms)

    def notify(self):
        # Callback from timer. Whenever timer calls, all blocks/obstacles step
        self._obstacle_manager.step()

    def start():
        self._timer.start()
        self.start_player_monitoring()

    def monitor_player(self):
        while True:
            blocks = [self._player] + self._obstacle_manager.obstacles
            user_input = display_blocks_and_get_user_input(self._arena, blocks, self._ui_title)
            


class Timer():
    def __init__(self, observer, timer_frequency_ms):
        self._observer = observer
        self._timer_frequency_s = timer_frequency_ms / 1000
        self.timer_thread = None
        self._timer_running = False

    def _timer_loop():
        while self._timer_running:
            time.sleep(self._timer_frequency_s)
            self._observer.notify()

    def start():
        self.timer_thread = threading.Thread(self._timer_loop, daemon=True)
        t.start()

    def stop():
        self._timer_running = False
        time.sleep(self._timer_frequency_s)
