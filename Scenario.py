class Slide:
    def __init__(self):
        self.timing = 0
        self.position = []
        self.velocity = []
        self.comment = []

    def set_velocity(self, array):
        self.velocity = array.copy()

    def set_position(self, array):
        self.position = array.copy()

    def set_timing(self, timing):
        self.timing = timing

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def get_timing(self):
        return self.timing

    def print(self):
        print("Timing is {0}".format(self.timing))

        print("Positions is:")
        for row in self.position:
            for col in row:
                print(col, end=' ')
            print()

        print("Velocity is:")
        for row in self.velocity:
            for col in row:
                print(col, end=' ')
            print()



class Scenario:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.type = 'square'
        self.name = 'Hello'
        self.slides = []
        self.slides.append(Slide())
        self.currentSlide = 0

    def set_rows(self, rows):
        self.rows = rows

    def set_cols(self, cols):
        self.cols = cols

    def set_name(self, name):
        self.name = name

    def get_num_of_slides(self):
        return len(self.slides)

    def set_current_slide(self, slideNum):
        self.currentSlide = slideNum

    def get_slide(self, index):
        try:
            return self.slides[index]
        except:
            return None

    def set_slide(self, slide, index):
        self.slides[index] = slide

    def append_slide(self, slide):
        self.slides.append(slide)

    def update_timings(self, startindex, delta):
        for i in range(startindex, len(self.slides)):
            self.slides[i].set_timing(self.slides[i].get_timing() + delta)

