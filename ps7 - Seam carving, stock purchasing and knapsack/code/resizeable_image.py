import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        """
            Evaluates the "best" seam. A vertical seam is a connected path of pixels,
            one pixel in each row. We call two pixels connected if they are
            vertically or diagonally adjacent. Best vertical seam is the one that
            minimizes the total “energy” of pixels in the seam.
            
            The funciton applies a bottom up approach starting from the top row,
            and going down.
            
            Parameters:
                imagematrix.ImageMatrix:   COMPLETE....
            
                                                     
        """
        # Set dp[:][0], noted that the notation of row and columns here is reversed,
        # meaning that the dp[i][j] refers to the element in the j'th row and i'th
        # column.
        #print(f'width = {self.width}')
        #print(f'height = {self.height}')
        dp = {}
        parents = {} 
        for i in range(self.width):
            dp[i,0] = self.energy(i,0)
        
        # Iterate over the rows starting from the first one
        
        for j in range(1,self.height):
            for i in range(self.width):
                current_energy = self.energy(i,j)
            # handle boundary conditions
                if i == 0:
                    dp[i,j] = min(dp[i,j-1],dp[i+1,j-1]) + current_energy
                    if dp[i,j-1] > dp[i+1,j-1]: parents[(i,j)] = (i+1,j-1)
                    else: parents[(i,j)] = (i,j-1)
                elif i == self.width - 1:
                    dp[i,j] = min(dp[i,j-1],dp[i-1,j-1]) + current_energy
                    if dp[i,j-1] > dp[i-1,j-1]: parents[(i,j)] = (i-1,j-1)
                    else: parents[(i,j)] = (i,j-1)
                else:
                    dp[i,j] = min(dp[i-1,j-1],dp[i,j-1],dp[i+1,j-1]) + current_energy
                    if dp[i,j-1] > dp[i-1,j-1]: 
                        if dp[i+1,j-1] > dp[i-1,j-1]: parents[(i,j)] = (i-1,j-1)
                        else: parents[(i,j)] = (i+1,j-1)
                    else:
                        if dp[i,j-1] > dp[i+1,j-1]: parents[(i,j)] = (i+1,j-1)
                        else: parents[(i,j)] = (i,j-1)
        last_row = [dp[i,self.height-1] for i in range(self.width)]                 
        best_index = last_row.index(min(last_row))
        
        tup = (best_index,self.height-1)
        best_seam = [tup]
        for j in range(self.height-1):
            best_seam.append(parents[tup])
            tup = parents[tup]
        best_seam.reverse()
        return best_seam
            
        
                
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
