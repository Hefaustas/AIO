import discord_rpc as rpc

import time
import threading


class DiscordRPC:
    initialized = False

    def __init__(self, client_id):
        self.rpc = rpc
        self.client_id = client_id
        self.running = False

    def connect(self):
        self.rpc.initialize(self.client_id)
        self.initialized = True

    def run_loop(self):
        def background_loop():
            while self.running:
                self.rpc.update_presence(
                    **{
                        'details': self.details,
                        'state': self.state,
                        'large_image_key': 'icon2',
                        'large_image_text': 'Eureka!',
                        'start_timestamp': self.start_time,
                    }

                )

                self.rpc.update_connection()
                time.sleep(2)

        self.running = True
        # self.running is to check if loop is running
        # create a separate thread so the program doesn't shit itself (hang) on the loop
        loop_thread = threading.Thread(target=background_loop)
        loop_thread.daemon = True
        loop_thread.start()

    def set_details(self, details):
        self.details = details

    def set_state(self, state):
        self.state = state

    def reset_time(self):
        self.start_time = time.time()

    def close(self):
        self.rpc.shutdown()
