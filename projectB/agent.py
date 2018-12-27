from PIL import Image, ImageChops, ImageFilter, ImageOps
import numpy as np
import random

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass
    
    def Solve(self, problem):
        
        
        if problem.problemType == '2x2':

            print("problem name: " + problem.name)
            prob_fig = {}
            ans_fig = {}
            prob_array = {}
            ans_array = {}
            
            
            rav_list = ['A', 'B', 'C']
            ans_list = ['1', '2', '3', '4', '5', '6']   
    
    
            for key in problem.figures:
                fig = problem.figures[key]
                image = Image.open(fig.visualFilename).convert('L')               
                arrayImage = self.centerImageArray(np.array(image))
                if key in rav_list:
                    prob_fig[key] = image
                    prob_array[key] = arrayImage
                if key in ans_list:
                    ans_fig[key] = image   
                    ans_array[key] = arrayImage          
            
            
            ATransformations = [ 
            self.centerImageArray(np.array(prob_fig['A'].transpose(Image.FLIP_LEFT_RIGHT))), 
            self.centerImageArray(np.array(prob_fig['A'].transpose(Image.FLIP_TOP_BOTTOM))), 
            self.centerImageArray(np.array(prob_fig['A'].transpose(Image.ROTATE_90))), 
            self.centerImageArray(np.array(prob_fig['A'].transpose(Image.ROTATE_180))), 
            self.centerImageArray(np.array(prob_fig['A'].transpose(Image.ROTATE_270)))
            ]
            
            BTransformations = [ 
            self.centerImageArray(np.array(prob_fig['B'].transpose(Image.FLIP_LEFT_RIGHT))), 
            self.centerImageArray(np.array(prob_fig['B'].transpose(Image.FLIP_TOP_BOTTOM))), 
            self.centerImageArray(np.array(prob_fig['B'].transpose(Image.ROTATE_90))), 
            self.centerImageArray(np.array(prob_fig['B'].transpose(Image.ROTATE_180))), 
            self.centerImageArray(np.array(prob_fig['B'].transpose(Image.ROTATE_270)))
            ]   
            
            CTransformations = [ 
            self.centerImageArray(np.array(prob_fig['C'].transpose(Image.FLIP_LEFT_RIGHT))), 
            self.centerImageArray(np.array(prob_fig['C'].transpose(Image.FLIP_TOP_BOTTOM))), 
            self.centerImageArray(np.array(prob_fig['C'].transpose(Image.ROTATE_90))), 
            self.centerImageArray(np.array(prob_fig['C'].transpose(Image.ROTATE_180))), 
            self.centerImageArray(np.array(prob_fig['C'].transpose(Image.ROTATE_270)))
            ]                    
        
                    
            
            if self.compare_images(prob_array['A'],prob_array['B']) == 0 or self.pixels_comparison(prob_array['A'],prob_array['B']) == 0:
                print('A == B')
                for i in range(1,7):
                    if self.compare_images(ans_array[str(i)], prob_array['C']) == 0 or self.pixels_comparison(ans_array[str(i)],prob_array['C']) == 0:
                        answer = i
                        print(answer)
                        return answer
            elif self.compare_images(prob_array['A'],prob_array['C']) == 0 or self.pixels_comparison(prob_array['A'],prob_array['C']) == 0:
                print('A == C')
                min_is_zero = []
                min_pix = []
                j = 0
                while  j < len(ans_array):
                    k = self.compare_images(ans_array[str(j+1)], prob_array['B'])
                    l = self.pixels_comparison(ans_array[str(j+1)], prob_array['B'])
                    min_is_zero.append(k)
                    min_pix.append(l)
                    j +=1                
                for i in range(1,7):
                        if self.compare_images(ans_array[str(i)], prob_array['B']) == 0 or self.pixels_comparison(ans_array[str(i)], prob_array['B']) == 0:
                            answer = i
                            print(answer)
                            return answer 
                        elif self.compare_images(ans_array[str(i)], prob_array['B']) != 0 and self.pixels_comparison(ans_array[str(i)], prob_array['B']) != 0:
                            answer = np.argmin(min_is_zero) + 1 
                            print(answer)
                            return answer
                        else:
                            return random.randint(1,7)
                    
                    
            elif self.compare_images(prob_array['A'],prob_array['C']) != 0 and self.pixels_comparison(prob_array['A'], prob_array['C']) != 0 :
                print('A !=C')
                compare_scoreAB = []
                compare_scoreCI = []
                compare_scoreAC = []
                compare_scoreBI = []
                i = 0
                compare_scoreAB = [ self.compare_images(x,prob_array['B']) for x in ATransformations]
                compare_scoreAC = [ self.compare_images(x,prob_array['C']) for x in ATransformations]
                print(compare_scoreAB)
                print(compare_scoreAC)
                index_minAB = np.argmin(compare_scoreAB)
                index_minAC = np.argmin(compare_scoreAC)
                transToCompare = CTransformations[index_minAB]
                transToCompareBI = BTransformations[index_minAC]
                compare_scoreCI = [ self.compare_images(ans_array[str(x)],transToCompare) for x in range(1,7)]
                compare_scoreBI = [ self.compare_images(ans_array[str(x)],transToCompareBI) for x in range(1,7)]
                print(compare_scoreCI)
                print(compare_scoreBI)
                
                if len(compare_scoreAB) == compare_scoreAB.count(compare_scoreAB[0]):
                    print('All equal')   
                    p = 0
                    mlist = []
                    while p < len(ans_array):
                        m = self.centerImageArray(np.array(ImageChops.darker(prob_fig['C'],ans_fig[str(p+1)])))
                        mlist.append(m)
                        p += 1
                        
                        
                    j = self.centerImageArray(np.array(ImageChops.darker(prob_fig['A'],prob_fig['B'])))
                    bcenter = self.centerImageArray(prob_array['B'])
                    k = self.compare_images(j, bcenter)
                    print(k)
                    
                    p1 = 0
                    complist = []
                    while p1 < len(ans_array):
                        z = self.compare_images(mlist[p1],ans_array[str(p1+1)])
                        complist.append(z)
                        p1 += 1
                        print(complist)
                        
                    mincomp = np.argmin(complist)
                    
                    if min(complist) <= k:
                        answer = mincomp + 1
                        print(answer)
                        return answer
                    else:
                        answer = mincomp + 1
                        print(answer)
                        return(answer)
    
                                    
                elif min(compare_scoreAC) < min(compare_scoreAB):
                    print('C transformation')
                    index_minCI = np.argmin(compare_scoreBI)
                    answer = index_minCI + 1
                    print(answer)
                    return answer
                elif min(compare_scoreAB) < min(compare_scoreAC):
                    print('B transformation')
                    index_minBI = np.argmin(compare_scoreCI)
                    answer = index_minBI + 1
                    print(answer)
                    return answer
                    
        
        
        if problem.problemType == '3x3':
            print('skipping')
            return - 1
