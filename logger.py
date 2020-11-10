class Logger:
    def __init__(self, filename, mode="a"):
        self.file = filename
        self.mode = mode
        self.writer = open(filename, mode=mode)
        self.closed = False

    def is_closed(self):
        return self.is_closed

    def close(self):
        if not self.closed:
            self.writer.close()
            self.closed = True

    def log(self, message: str):
        self.writer.write(message)
        self.writer.write("\n")

    def clear(self):
        self.writer.seek(0)
        self.writer.truncate()
