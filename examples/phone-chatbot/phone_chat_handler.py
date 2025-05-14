import time
import threading

class PhoneChatHandler:
    def __init__(self):
        self.call_start_time = time.time()
        self.last_speech_time = time.time()
        self.silence_events = 0
        self.unanswered_prompts = 0
        self.max_unanswered = 3
        self.running = True

        self.monitor_thread = threading.Thread(target=self.monitor_silence)
        self.monitor_thread.start()

    def on_audio_input(self, audio):
        self.last_speech_time = time.time()

    def monitor_silence(self):
        while self.running:
            time.sleep(2)
            if time.time() - self.last_speech_time > 10:
                self.handle_silence()

    def handle_silence(self):
        self.silence_events += 1
        self.unanswered_prompts += 1
        print("TTS: Are you still there?")
        self.last_speech_time = time.time()
        if self.unanswered_prompts >= self.max_unanswered:
            print("TTS: Ending call due to no response.")
            self.end_call()

    def end_call(self):
        self.running = False
        self.summarize()

    def summarize(self):
        duration = int(time.time() - self.call_start_time)
        print(f"\n📞 CALL SUMMARY\n- Duration: {duration}s\n- Silence Events: {self.silence_events}\n- Unanswered: {self.unanswered_prompts}\n")
