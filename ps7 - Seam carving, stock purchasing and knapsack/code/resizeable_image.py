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
            
            Pixel images i,j refer to an element in the j'th row and i'th
            column.
            
            Parameters:
                self.width: int, image width
                self.height: int,  image height
                self.energy: function, evaluates the energy of the (i,j) pixel
                                    of the image
                dp: dict, mapping pairs i,j to the accumulated energy of the best
                            seam ending in pixel (i,j)
            Returns:
                best_seam: list, containing tuples (i,j) from j=0 
                                to j = self.width - 1, indicating the pixels
                                of the best vertical seam.
        """
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
                # pixel in the interior of the image
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
        
        # following the parent pointers evaluate the best seam (following the
        # topological sort in reverse order).
        tup = (best_index,self.height-1)
        best_seam = [tup]
        for j in range(self.height-1):
            best_seam.append(parents[tup])
            tup = parents[tup]
        best_seam.reverse()
        return best_seam
            
        
                
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
