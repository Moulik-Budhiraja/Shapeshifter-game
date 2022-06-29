class Animation:
    def __init__(self, image, frames):
        self.image = image
        self.frames = frames
        self.original_frames = frames

    def copy(self):
        return Animation(self.image, self.original_frames)

    def __repr__(self):
        return f'Animation({self.image}, {self.frames})'
