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
        
                    
            
            if self.compare_images(prob_array['A'],prob_array['B']) == 0:
                print('A == B')
                for i in range(1,7):
                    if self.compare_images(ans_array[str(i)], prob_array['C']) == 0:
                        answer = i
                        print(answer)
                        return answer
            elif self.compare_images(prob_array['A'],prob_array['C']) == 0:
                print('A == C')
                min_is_zero = []
                j = 0
                while  j < len(ans_array):
                    k = self.compare_images(ans_array[str(j+1)], prob_array['B'])
                    min_is_zero.append(k)
                    j +=1                
                for i in range(1,7):
                        if self.compare_images(ans_array[str(i)], prob_array['B']) == 0:
                            answer = i
                            print(answer)
                            return answer 
                        elif self.compare_images(ans_array[str(i)], prob_array['B']) != 0:
                            answer = np.argmin(min_is_zero) + 1 
                            print(answer)
                            return answer
                        else:
                            return random.randint(1,7)
                    
                    
            elif self.compare_images(prob_array['A'],prob_array['C']) != 0:
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
                                                               
                                
                                
                                
                              

    
    def solve3x3(self, problem):
        pass
                                 
    def centerImageArray(self,figArray):
        figImage = Image.fromarray(figArray, "L")
    
        # mask
        threshold=128
        mask = figImage.point(lambda p: p < threshold and 255)
    
        # find edges
        edges = mask.filter(ImageFilter.FIND_EDGES)
        box = edges.getbbox()
        edges = edges.crop(box)
    
        # center in new image-figure
        tempImg = Image.new("L", figImage.size)
    
        width, height = edges.size
        fwidth, fheight = figImage.size
    
        tempImg.paste(edges, ((fwidth - width) // 2, (fheight - height) // 2))
    
        return np.array(tempImg)
    
    def MSE(self,arrayA, arrayB):
        return np.square(arrayA - arrayB).mean()
    
    def compare_images(self, arrayA, arrayB):
        # compute the mean squared error and structural similarity
        # index for the images
        m = self.MSE(arrayA, arrayB)
        return m
    
    def getFigureDarkpixels(self, figArray, figArray2):
        # in 'L', 255 is white
        white1 = np.count_nonzero(figArray)
        black1 = figArray.size - white1
        white2 = np.count_nonzero(figArray2)
        black2 = figArray2.size - white2
        difference = abs(black2 - black1)
        return difference     
    
    def find_min(self, arrayA, arrayB, arrayC, ans_array):
        
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
        
    
        compare_scoreAB = []
        compare_scoreCI = []
        for x in range(len(ATransformations)):
            compare_scoreAB.append(self.compare_images(ATransformations[x],prob_array['B']))
            if compare_scoreAB[x] == min(compare_scoreAB):
                trans_index = x
                for i in range(1,9):
                    compare_scoreCI.append(self.compare_images(CTransformations[trans_index], ans_array[str(i)]))
                    if compare_scoreCI[str(i)] == min(compare_scoreCI):
                        answer = i
                        return answer
                    
                    
    def image_combo(self, prob_fig, prob_array, ans_fig, ans_array):
        AB = self.centerImageArray(np.array(ImageChops.darker(prob_fig['A'],prob_fig['B'])))
        BC = self.centerImageArray(np.array(ImageChops.darker(prob_fig['B'],prob_fig['C'])))
        AC = self.centerImageArray(np.array(ImageChops.darker(prob_fig['B'],prob_fig['C'])))
    
        GH = []
        HI = []
        GI = []
        i = 0
        while i < len(ans_array):
            GH.append(self.centerImageArray(np.array(ImageChops.darker(prob_fig['G'],ans_fig[str(i)]))))
            HI.append(self.centerImageArray(np.array(ImageChops.darker(prob_fig['H'],ans_fig[str(i)]))))
            GI.append(self.centerImageArray(np.array(ImageChops.darker(prob_fig['G'],ans_fig[str(i)]))))
            i += 1
            
        if AB == prob_array['C']:
            g = 0
            while g < len(GH):
                if GH[g] == ans_array[str(g + 1)]:
                    answer = g + 1
                    print(answer)
                    g += 1
                    return answer
                
        elif BC == prob_array['A']:
            g = 0
            while g < len(HI):
                if HI[g] == ans_array[str(g + 1)]:
                    answer = g + 1
                    print(answer)
                    g += 1
                    return answer
                
        elif AC == prob_array['B']:
            g = 0
            while g < len(GI):
                if GI[g] == ans_array[str(g + 1)]:
                    answer = g + 1
                    print(answer)
                    g += 1
                    return answer
    
    def cyclic_patterns(self, prob_fig, prob_array, ans_fig, ans_array):
        if A == E:
            for i in range(1,9):
                if ans_array[str(i)] == prob_array['E']:
                    answer = i
                    print(answer)
                    return(answer)
                
    def image_difference(self, prob_fig, prob_array, ans_fig, ans_array):
        
        diffAB= ImageChops.difference(prob_fig['A'], prob_fig['B'])
        diffarrayAB = centerImageArray(np.array(diffAB))
        diffGH = ImageChops.difference(prob_fig['G'], prob_fig['H'])
        diffarrayGH = centerImageArray(np.array(diffGH))        
        
        if diffarrayAB.all() == prob_array['C'].all():
            for i in range(1,9):
                if diffarrayGH.all() == ans_array[str(i)]:
                    answer = i
                    print(answer)
                    return answer
        
    def make_transparent(self,prob_fig, ans_fig):
        
        datas = img.getdata()
        
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        
        
    def pixel_count_pattern(self):
        
        ab = self.getFigureDarkpixels(prob_array['A'], prob_array['B'])
        bc = self.getFigureDarkpixels(prob_array['B'], prob_array['C'])
        de = self.getFigureDarkpixels(prob_array['D'], prob_array['E'])
        ef = self.getFigureDarkpixels(prob_array['E'], prob_array['F'])
        gh = self.getFigureDarkpixels(prob_array['G'], prob_array['H'])
        
        if ab == de:
            if bc == ef:
                if ab == gh:
                    for i in range(1,9):
                        if self.getFigureDarkpixels(ans_array[str(i)], prob_array['H']) == bc:
                            answer = i
                            print(answer)
                            return answer
