import time
import threading


class PhoneChatHandler:
    def __init__(self):
        self.start_time = time.time()
        self.last_heard = time.time()
        self.silence_count = 0
        self.prompt_count = 0
        self.prompt_limit = 3
        self.active = True

        # Start background thread to monitor silence
        self._monitor = threading.Thread(target=self._watch_for_silence)
        self._monitor.daemon = True
        self._monitor.start()

    def on_audio_input(self, audio_data: bytes):
        """Resets the silence timer when user input is received."""
        self.last_heard = time.time()

    def _watch_for_silence(self):
        while self.active:
            time.sleep(2)
            if time.time() - self.last_heard > 10:
                self._respond_to_silence()

    def _respond_to_silence(self):
        self.silence_count += 1
        self.prompt_count += 1
        print("TTS: Are you still there?")
        self.last_heard = time.time()

        if self.prompt_count >= self.prompt_limit:
            print("TTS: Ending call due to no response.")
            self.end_call()

    def end_call(self):
        self.active = False
        self._log_summary()

    def _log_summary(self):
        total_duration = int(time.time() - self.start_time)
        print("\n📞 CALL SUMMARY")
        print(f"- Duration: {total_duration} seconds")
        print(f"- Silence Events: {self.silence_count}")
        print(f"- Unanswered Prompts: {self.prompt_count}")
