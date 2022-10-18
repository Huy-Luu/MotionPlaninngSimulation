import numpy as np

class SlidingWindow:
    def __init__(self, size):
        self.size = size
        print("The size is: " + str(size))

    def plot(self, plt):
        outline = np.array([[-self.size, -self.size, self.size, self.size, -self.size],
                    [-self.size, self.size, self.size, -self.size, -self.size]])
                    
        plt.plot(np.array(outline[0, :]).flatten(),
                    np.array(outline[1, :]).flatten())
