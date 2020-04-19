import time
import threading
from .blocks import Block
from .obstacles_and_players import ObstacleManager, Player
from .ui import display_blocks_and_get_user_input, close_all_windows


class CarRaceEngine():
    def __init__(self, config):
        self._ui_title = config["ui_title"]
        self._left_arrow_key = config["left_arrow_key"]
        self._right_arrow_key = config["right_arrow_key"]

        self._timer = Timer(self, config["obstacle_move_ms"])
        self.obstacle_speed_increase_interval_s = config["obstacle_speed_increase_interval_s"]
        self.obstacle_step_increment = config["obstacle_step_increment"]
        # print("CarEngine: Creating Arena")
        self._arena = Block.from_width_height(config["arena_width"], config["arena_height"])
        # print("CarEngine: Creating Obstacle Manager")
        obstacle_meta = {"color": config["obstacle_color"]}
        self._obstacle_manager = ObstacleManager(self._arena, config["max_obstacles"],
                                                 config["obstacle_width"], config["obstacle_height"],
                                                 obstacle_meta,
                                                 config["obstacle_step_size"],
                                                 config["obstacle_min_dist"],
                                                 config["obstacle_max_dist"])
        player_meta = {"color": config["player_color"]}
        self._player = Player.from_width_height(config["obstacle_width"], config["obstacle_height"],
                                                config["player_step_size"], player_meta,
                                                boundary=self._arena)
        self._t_last_step_size_update = time.time()

    def notify(self):
        # print("\n\n\nCarEngine: Timer Called. Calling obstacle mamager to move")
        # Callback from timer. Whenever timer calls, all blocks/obstacles step
        self._obstacle_manager.step()
        if time.time() - self._t_last_step_size_update > self.obstacle_speed_increase_interval_s:
            self._obstacle_manager.increment_step_size(self.obstacle_step_increment)
            print("Increasing speed")
            self._t_last_step_size_update = time.time()

    def start(self):
        # print("CarEngine: Starting Game...")
        self._timer.start()
        self.monitor_player()
        # print("CarEngine: Stopping...")
        self._timer.stop()
        close_all_windows()
        # print("CarEngine: Stopped...")

    def monitor_player(self):
        while True:
            blocks = [self._player] + self._obstacle_manager.obstacles
            user_input = display_blocks_and_get_user_input(self._arena, blocks, self._ui_title)
            if user_input == self._left_arrow_key:
                self._player.step_left()
            elif user_input == self._right_arrow_key:
                self._player.step_right()
            elif user_input == ord('q'):
                break
            if self._obstacle_manager.overlap_any_obstacle(self._player):
                blocks = [self._player] + self._obstacle_manager.obstacles
                display_blocks_and_get_user_input(self._arena, blocks, self._ui_title)
                print("Player collided with obstacle")
                break


class Timer():
    def __init__(self, observer, timer_frequency_ms):
        self._observer = observer
        self._timer_frequency_s = timer_frequency_ms / 1000
        self._timer_running = False

    def _timer_loop(self):
        self._timer_running = True
        while self._timer_running:
            time.sleep(self._timer_frequency_s)
            self._observer.notify()

    def start(self):
        threading.Thread(target=self._timer_loop, daemon=True).start()

    def stop(self):
        self._timer_running = False
        time.sleep(self._timer_frequency_s)


if __name__ == "__main__":
    import json
    with open("config.json", "r") as f:
        config = json.load(f)
    
    engine = CarRaceEngine(config)
    engine.start()