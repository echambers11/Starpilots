from title import Title

class Timer(Title):
    def __init__(self, game, center, time):
        super().__init__(game, '', center, text_size=35)
        self.start_time = time

    def _update(self, time):
        self.secs = (time - self.start_time) // 1000
        mins = int(self.secs // 60)
        secs = self.secs % 60
        elapsed_time = f"{mins}:{secs:02}"
        self._prep_msg(elapsed_time, self.rect.center)

    def draw(self, time = None):
        if time:
            self._update(time)
        self.screen.blit(self.msg_image, self.rect)