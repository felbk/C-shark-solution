import matplotlib.pyplot as plt

def gerarGraficos(filename=str, x = list , heights = list ):

    plt.bar(x,heights,0.8 , color= "#207d60")
    for i, v in enumerate(heights):
        plt.text(i, v + 0.03*max(heights), str(int(v)), ha='center')
    for i, v in enumerate(x):
        plt.text(i, -max(heights)*0.03, str(v), ha='center')
    
    plt.gca().set_axis_off()

    #plt.show()
    plt.savefig(filename)


