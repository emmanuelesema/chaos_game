import numpy as np
import matplotlib.pyplot as plt

class ChaosGame:
    def __init__(self, n, r):
        self.n = n
        self.r = r
        
        if (n < 3):
            raise ValueError ("n value is less than 3!")
        if (r < 0 or r > 1):
            raise ValueError ("r value is less than 0 or greater than 1!")
        self._generate_ngon()

    def _generate_ngon(self): 
        """Generating the points for the shape"""
        n = self.n
        r = self.r
        angle = (2 * np.pi) / n
        corners = []
        
        for i in range(n):
            corners.append ( [float(np.sin(i * angle)), float(np.cos(i * angle))] )
        #print(corners)
        return corners
        
    def plot_ngon(self):
        """Plotting the initial points for the shape"""
        corners = self._generate_ngon()
        plt.scatter(*zip(*corners))
        
    def _starting_point(self):
        """Creating starting points iteration for points in shape"""
        corners = self._generate_ngon()
        
        #print(corners)
        cx_values = []
        cy_values = []
        w = []
        
        N = 1 #number of points/w values to create
        
        for d in range(N):
            
            w2 = np.random.random(len(corners))
            w2 /= w2.sum()
            w.append(w2)
        #print("w := ",w)
        #print()
        
        for i in range (0, len(corners)):
            """Unpacking x and y corners value to multiply"""
            cx_values2 = corners[i][0]
            cy_values2 = corners[i][1]
            
            cx_values.append(cx_values2)
            cy_values.append(cy_values2)
        
        #print(cx_values)
        #print(cy_values)
        #print()
        
        X = np.zeros((N,2)) #2xn array
        for i in range(N):
            Xx = 0
            Xy = 0
            for k in range(len(corners)):
                """Multiplying and finding X0 with w_i values with corners 
                            x and y values then plotting"""
                
                Xx +=  (w[i][k]) * (cx_values[k]) #x values of X
                Xy +=  (w[i][k]) * (cy_values[k]) #y values of X"""
            #print(Xx,Xy)
            X[i,:] = np.array([Xx, Xy])
        return X
        
    def iterate(self, steps, discard=5):
        """Iterating starting from the starting point [from _starting_point()] 
                                withing the shape"""
        self.steps = steps
        r = self.r
        corners = self._generate_ngon()
        X = np.zeros((steps,2)) #2xn array
        X[0,:] = self._starting_point()
        
        cj = np.zeros((steps,2)) #2 x steps array
        
        J = np.zeros((steps,3))
        #print('Steps =: ',steps)
        for j in range(steps):
            R = (np.random.randint(len(corners)))

            cj[j,:] = np.array([corners[R][0], corners[R][1]])
            #print(cj)
            if R == 0:
                J[j:,R] = 1
                J[j:,1] = 0
                J[j:,2] = 0
            elif R == 1:
                J[j:,R] = 1
                J[j:,R-1] = 0
                J[j:,R+1] = 0
            elif R == 2:
                J[j:,R] = 1
                J[j:,0] = 0
                J[j:,1] = 0

        #print('J =: ',J)
        #print('Cj =: ',cj)
        #print('-----------')
        self.J = J
        
        for i in range(steps-1):
            
            X[i+1,:] = r * X[i,:] + (1 - r) * cj[i,:]
            
        #print('X =: ',X)
        self.X = X
        return X

    def plot(self, color=False, cmap="jet"):
        """Plotting the color and points of the shape"""
        X = self.iterate(self.steps)
        #print(X)
        #print('C in plot =: ',self.gradient_color)
        if color == True:
            colors = self.gradient_color
        elif color == False:
            colors = 'black'
        #print('X here =: ',X)
        plt.scatter(X[:,0], X[:,1], c=colors, cmap = cmap, s=0.2)
        plt.axis('equal')
        plt.axis('off')

    def show(self, color=False, cmap="jet"):
        """Showing the shape"""
        self.plot(color, cmap)
        plt.axis('equal')
        plt.axis('off')
        plt.show()
        return 
    
    @property
    def gradient_color(self):
        """Property calculating the changing colors for the different 
                        colors in the shape"""
        steps = self.steps
        #print('n value =: ',steps)
        J = self.J
        C = np.zeros((steps,3))

        #print('J value =:',J)
        for i in range(steps-1):
            C[0,:] = J[0]
            C[i+1,:] = (C[i,:] + J[i+1])/ 2
        #print('Gradient color (@property) =: ',C)
        return C
    
    def savepng(self, outfile, color=False, cmap="jet"):
        """Saving the image as a .png file"""

        self.plot(color)
        
        for i in range(1,len(outfile)):

            if (outfile[-i] == '.'):
                t = outfile[-i:]
                #print('t =: ',t)
                if (t != '.png'):
                    raise ValueError(f'The format {t} is not accepted!')
                    return
                if(outfile[-4:] == '.png'):
                    print('.png was specified')
                    plt.savefig(f'{outfile}',dpi = 300 )
                    return
        else:
            print('.png was not specified')
            plt.savefig(f'{outfile}.png',dpi = 300)
        return

    
if __name__ == '__main__':
    tri = ChaosGame(3, 0.5)
    tri._generate_ngon()
    tri.plot_ngon() 
    tri._starting_point()
    tri.iterate(10000, discard=5)
    tri.show(color=True)
    tri.savepng('chaos{1}.png',color=True)
    
if __name__ == '__main__':
    tri = ChaosGame(4, 1/3)
    tri._generate_ngon()
    tri.plot_ngon() 
    tri._starting_point()
    tri.iterate(10000, discard=5)
    tri.show(color=True)
    tri.savepng('chaos{2}.png', color=True)

if __name__ == '__main__':
    tri = ChaosGame(5, 1/3)
    tri._generate_ngon()
    tri.plot_ngon() 
    tri._starting_point()
    tri.iterate(10000, discard=5)
    tri.show(color=True)
    tri.savepng('chaos{3}.png', color=True)
    
if __name__ == '__main__':
    tri = ChaosGame(5, 3/8)
    tri._generate_ngon()
    tri.plot_ngon() 
    tri._starting_point()
    tri.iterate(10000, discard=5)
    tri.show(color=True)
    tri.savepng('chaos{4}.png', color=True)

if __name__ == '__main__':
    tri = ChaosGame(6, 1/3)
    tri._generate_ngon()
    tri.plot_ngon() 
    tri._starting_point()
    tri.iterate(10000, discard=5)
    tri.show(color=True)
    tri.savepng('chaos{5}.png', color=True)