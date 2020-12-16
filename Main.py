#Sinclair Fuh, 12/13/2020
#Coding Sample for Mathematica: Iris Visualization

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from functools import reduce

class MainWindow:
    def __init__(self):
        #Variables used for managing data.
        #sample size is the sample size for each species of flower.
        #Cur_index is the index used to retrieve the name of the current statistic being displayed. from Value_Names
        #Value names is a list of every type of statistic avaliable. ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        #Flower names is a list of every species of flower. ['Setosa', 'Versicolor', 'Virginicum']
        self.iris = sns.load_dataset("iris")
        self.sample_size = 50
        self.cur_index = 0
        self.Value_names = self.iris.columns.values[:4]
        self.Flower_Names = self.iris['species'].unique()

        #Variables used for drawing the graph
        self.fig, self.axs = plt.subplots(1, 3)
        self.color_names = ['tab:pink', 'tab:cyan', 'tab:olive']
        plt.subplots_adjust(bottom=0.2)

        #"Previous" and "Next" buttons are contained within two different axes
        axprev = plt.axes([0.20, 0.05, 0.15, 0.075])
        bprev = Button(axprev, 'Previous Trait')
        bprev.on_clicked(self.prev)

        axnext = plt.axes([0.70, 0.05, 0.15, 0.075])
        bnext = Button(axnext, 'Next Trait')
        bnext.on_clicked(self.next)
        self.draw_graph()


    #decrements index and redraws graphs
    def prev(self, event):
        if self.cur_index == 0:
            self.cur_index = 3
        else:
            self.cur_index -= 1

        self.draw_graph()

    #increments index and redraws graphs
    def next(self, event):
        if self.cur_index == 3:
            self.cur_index = 0
        else:
            self.cur_index += 1

        self.draw_graph()

    #A method that's called whenever the graph needs to be redrawn. It draws the current statistic according to Value_names[cur_index] for
    #each species of flower.
    def draw_graph(self):

        for ax in self.axs:
            ax.clear()

        #name of the current statistic being displayed
        cur_value = self.Value_names[self.cur_index]

        #goes through each flower name and draws their statistics on the appropriate subplot
        for i in range(0,len(self.Flower_Names)):

            #cur_flower: name of the current flower being looked at
            #cur_values: a list of the sizes for the current statistic of the current flower.
            #cur_min: the min. size in cur_values
            #cur_max: the max. size in cur_values.
            #cur_min and cur_max are used to plot the x-axis for each graph.
            cur_flower = self.Flower_Names[i]
            cur_values = self.iris[self.iris['species'] == cur_flower][cur_value].values
            cur_min = round(min(cur_values), 1)
            cur_max = round(max(cur_values), 1)
            graph = self.axs[i]

            print("Currently drawing {}'s {}: max: {}. min: {}".format(cur_flower, self.Value_names[self.cur_index], cur_max, cur_min))
            print(cur_values)

            bin_size = self.get_bin_size(round((cur_max-cur_min)*10, 0))
            #Since numpy arrays were unreliable for generating bins, I had to use a list function as a workaround.
            bins = [round(x*0.1, 1) for x in range(int(cur_min*10), int(cur_max*10) + int(bin_size*10), int(bin_size*10))]
            graph.set_xticks(bins)
            hist_data = graph.hist(cur_values, bins = bins, label = cur_flower, rwidth = 0.9, color = self.color_names[i])

            #sets Y axis based on max. Y value of histogram
            Y_max = int(max(hist_data[0]))
            graph.set_yticks([x for x in range(0, Y_max+2, 2)])

            graph.set_title(label="Species: {}".format(cur_flower), fontsize = 8)
            self.fig.suptitle("{} statistics".format(cur_value.replace('_', ' ')))
            if i == 0:
                graph.set_ylabel('occurences (per sample size of 50)')

                graph.set_xlabel('{} size (inches)'.format(cur_value.replace('_', ' ')))

        plt.draw()
        plt.show()

    #efficient method for returning a list of all factors of a number.
    #https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
    def factors(self, n):
        return reduce(list.__add__,
                          ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0))


    # code for dynamically choosing bin size based on all possible factors of the bin range. diff/bin_size must be between 5 and 10,
    #and diff%bin_size must be 0.
    #input: the difference between min_value and max_value
    #output: the most appropriate bin_size
    def get_bin_size(self, diff):
        factors = self.factors(diff)
        #removes diff from the list of factors
        factors = factors[:len(factors)-1]
        cur_index = 0

        #base case: diff is a prime number
        if len(factors) == 1:
            return round(factors[0]/10, 1)

        while True:
            bins = diff/factors[cur_index]
            if bins >= 5 and bins <= 10:
                return round(factors[cur_index]/10, 1)

            #worst case: return 0.1 as the appropriate bin size
            if cur_index == len(factors)-1:
                return round(0.1, 1)

            cur_index += 1







if __name__ == '__main__':
    MainWindow()




