numberOfBalls = 10
ballsXRow = 10
ballsYRow = 0

position = [0 for i in range(numberOfBalls)]
t = 0


def linear_delay(pos, delay, speed):
    global t
    global position
    for i in range(numberOfBalls):
        position[i] = pos
        print("{0}: {1}".format(t, position))
        t += delay


linear_delay(100, 500, 30)
