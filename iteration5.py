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
        
                    
            
            if self.compare_images(prob_array['A'],prob_array['B']) == 0 or self.getFigureDarkpixels(prob_array['A'],prob_array['B']) == 0:
                print('A == B')
                for i in range(1,7):
                    if self.compare_images(ans_array[str(i)], prob_array['C']) == 0 or self.getFigureDarkpixels(ans_array[str(i)],prob_array['C']) == 0:
                        answer = i
                        print(answer)
                        return answer
            elif self.compare_images(prob_array['A'],prob_array['C']) == 0 or self.getFigureDarkpixels(prob_array['A'],prob_array['C']) == 0:
                print('A == C')
                min_is_zero = []
                min_pix = []
                j = 0
                while  j < len(ans_array):
                    k = self.compare_images(ans_array[str(j+1)], prob_array['B'])
                    l = self.getFigureDarkpixels(ans_array[str(j+1)], prob_array['B'])
                    min_is_zero.append(k)
                    min_pix.append(l)
                    j +=1                
                for i in range(1,7):
                        if self.compare_images(ans_array[str(i)], prob_array['B']) == 0 or self.getFigureDarkpixels(ans_array[str(i)], prob_array['B']) == 0:
                            answer = i
                            print(answer)
                            return answer 
                        elif self.compare_images(ans_array[str(i)], prob_array['B']) != 0 and self.getFigureDarkpixels(ans_array[str(i)], prob_array['B']) != 0:
                            answer = np.argmin(min_is_zero) + 1 
                            print(answer)
                            return answer
                        else:
                            return random.randint(1,7)
                    
                    
            elif self.compare_images(prob_array['A'],prob_array['C']) != 0 and self.getFigureDarkpixels(prob_array['A'], prob_array['C']) != 0 :
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
            
                print("problem name: " + problem.name)
                prob_fig = {}
                ans_fig = {}
                prob_array = {}
                ans_array = {}
                
                
                rav_list = ['A', 'B', 'C','D','E','F','G','H']
                ans_list = ['1', '2', '3', '4', '5', '6','7','8']   
        
        
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
                        
            
                        
                if self.compare_images(prob_array['A'],prob_array['B']) == 0:
                    print('A == B')
                    for i in range(1,9):
                        if self.compare_images(ans_array[str(i)], prob_array['H']) == 0:
                            answer = i
                            print(answer)
                            return answer
                        else:
                            m = self.find_min(ans_array, prob_array['H'])
                            answer = m + 1
                            print(answer)
                            return answer
                       
                
                elif self.getFigureDarkpixels(prob_array['A'],prob_array['E']) == 0 or self.getFigureDarkpixels(prob_array['A'],prob_array['E'])==0:
                    print('Cyclic pattern')
                    m = self.image_combo(prob_fig, prob_array)
                    print(m[1])
                    if m[0] < self.compare_images(prob_array['A'], prob_array['E']):
                        answer = self.ans_combo(ans_fig,ans_array, prob_fig, prob_array, m[1])
                        return answer                        
                    else:
                        for i in range(1,9):
                            if self.compare_images(prob_array['E'],ans_array[str(i)]) == 0 or self.getFigureDarkpixels(prob_array['E'],ans_array[str(i)]) == 0:
                                answer = i
                                print(answer)
                                return answer
                            else:
                                m = self.find_min(ans_array, prob_array['E'])
                                answer = m + 1
                                print(answer)
                                return answer
                            
                elif self.getFigureDarkpixels(prob_array['A'], prob_array['E']) < self.getFigureDarkpixels(prob_array['A'],prob_array['B']):
                    if self.getFigureDarkpixels(prob_array['A'], prob_array['E']) < self.getFigureDarkpixels(prob_array['A'],prob_array['C']):
                        print("another cyclic pattern")
                        h = self.cyclic_pattern(prob_fig, prob_array, ans_fig, ans_array)
                        print(h)
                        sec_min = self.find_second_min(ans_array,prob_array['E'])
                        result = sec_min[1]
                        for i in range(1,9):
                            if self.getFigureDarkpixels(ans_array[str(i)],prob_array['E']) == h:
                                if h == 0:
                                    answer = result
                                    print(answer)
                                    return answer
                                else:
                                    answer = i
                                    print(answer)
                                    return answer
                            
                                    
                elif self.difference_of_difference(prob_array['A'],prob_array['D'],prob_array['B'],prob_array['E'],prob_array['C'],prob_array['F']) == 0:
                    print('outter image same in columns inner image same in rows')
                    m = self.image_combo(prob_fig, prob_array)
                    print(m[0])
                    print(m[1])
                    if m[0] < self.compare_images(prob_array['B'], prob_array['C']):
                        answer = self.ans_combo(ans_fig,ans_array, prob_fig, prob_array, m[1])
                        return answer
                    else:
                        for i in range(1,9):
                            if self.difference_of_difference(prob_array['F'],ans_array[str(i)],prob_array['E'],prob_array['H'],prob_array['D'],prob_array['G']) < 1:
                                answer = i
                                print(answer)
                                return answer
                
                elif self.difference_of_difference(prob_array['A'],prob_array['B'],prob_array['D'],prob_array['E'],prob_array['G'],prob_array['H']) <= 1:
                    print('Same transformation across rows')
                    m = self.image_combo(prob_fig, prob_array)
                    print(m[0])
                    print(m[1])
                    print(self.compare_images(prob_array['B'], prob_array['C']))
                    if m[0] < self.compare_images(prob_array['B'], prob_array['C']):
                        answer = self.ans_combo(ans_fig,ans_array,prob_fig,prob_array, m[1])
                        return answer
                    else:
                        for i in range(1,9):
                            if self.difference_of_difference(prob_array['H'],ans_array[str(i)],prob_array['E'],prob_array['F'],prob_array['B'],prob_array['C']) <= 1:
                                answer = i
                                print(answer)
                                return answer
                                    
                                                                                                                  
                elif self.compare_images(prob_array['B'], prob_array['D']) == 0:
                    if self.compare_images(prob_array['C'], prob_array['E']) == 0:
                        print('Increasing Pattern')
                        m = self.greater_than_list
                        for i in range(len(m)):
                            if m[i] == min(m):
                                answer = i
                                return answer
                else:
                   print('Guessing')
                   answer = random.randint(1,9)
                   print(answer)
                   return answer
                
                                         
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
    
    def find_min(self, ans_array, array2):
            answer_compare = [self.compare_images(ans_array[str(x+ 1)],array2) for x in range(len(ans_array))]
            min_array = np.argmin(answer_compare)
            return min_array
    
    def find_second_min(self, ans_array, array2):
        answer_compare = [self.compare_images(ans_array[str(x+ 1)],array2) for x in range(len(ans_array))]
        answer_compare1 = answer_compare
        answer_compare1.sort()
        length = len(answer_compare)
        second_smallest = answer_compare1[length - 2]
        
        for i in range(length):
            if answer_compare[i] == second_smallest:
                answer = i
        
        answer_comparepix = [self.getFigureDarkpixels(ans_array[str(x+ 1)],array2) for x in range(len(ans_array))]
        answer_comparepix1 = answer_comparepix
        answer_comparepix1.sort()
        length1 = len(answer_comparepix)
        second_smallestpix = answer_comparepix1[length - 2]
        
        for i in range(length1):
            if answer_comparepix[i] == second_smallestpix:
                answerpix = i
                
                resultlist = [answer,answerpix]
                return resultlist        
    
    
    def cyclic_pattern(self, prob_fig, prob_array, ans_fig, ans_array):
        aList = ["AB", "AC", "AD", "AE","AF"]
        bList = ["BC","BD","BE","BF"]
        cList = ["CD","CE","CF"]
        acompare = [ prob_array['B'],prob_array['C'],prob_array['D'],prob_array['E'],prob_array['F']]
        bcompare = [prob_array['C'],prob_array['D'],prob_array['E'],prob_array['F']]
        ccompare = [prob_array['D'],prob_array['E'],prob_array['F']]
        
        
        aDict = [self.getFigureDarkpixels(prob_array['A'],x) for x in acompare]
        bDict = [self.getFigureDarkpixels(prob_array['B'],x) for x in bcompare]
        cDict = [self.getFigureDarkpixels(prob_array['C'],x) for x in ccompare]
        
        
        print(aDict)
        print(bDict)
        print(cDict)
            
        aMin = min(aDict)
        print(aMin)
        bMin = min(bDict)
        print(bMin)
        cMin = min(cDict)
        print(cMin)
        
        Elist = [self.getFigureDarkpixels(ans_array[str(x)],prob_array['E']) for x in range(1,9)]
        print(Elist)
        Emin = min(Elist)
        print(Emin)
        
        
        if aMin == aDict[3]:
            print('AE')
            result = Emin
            return result                                
        elif aMin == aDict[4]:
            print('AF')
            result = Emin
            return result
        else:
            return Emin
         
        
            
        
    def find_nearest_neighbor(self, answer_array, prob_array):
        answer_compare = [self.compare_images(ans_array[str(x+ 1)],prob_array['D']) for x in range(len(ans_array))]
        prob_pixels = self.getFigureDarkpixels(prob_fig['E'],prob_fig['H'])
        nearest_list = [abs(prob_pixels - answer_compare[x]) for x in range(len(answer_compare))]
        nearestNeighbor = np.argmin[nearest_list]
        answer = nearestNeighbor + 1
        print(answer)
        return answer
    
    def difference_of_difference(self, array1, array2, array3, array4,array5,array6):
        m = self.getFigureDarkpixels(array1, array2)
        n = self.getFigureDarkpixels(array3, array4)
        o = self.getFigureDarkpixels(array5, array6)
        
        diff_of_diff1 = abs(m - n)
        diff_of_diff2 = abs(n - o)
        diff = diff_of_diff2 - diff_of_diff1
        if diff == 0:
            return 0
        else:
            if diff_of_diff1 != 0:
                result = diff/diff_of_diff1
                return result
            else:
                result = diff/diff_of_diff2
                return result
            
        
    def greater_than_list(self, ans_array, prob_array):
        
        if self.getFigureDarkpixels(prob_array['A'],prob_array['B']) < self.getFigureDarkpixels(prob_array['B'],prob_array['C']):
            i = 0
            max_list = []
            while i < len(ans_array):
                m = self.getFigureDarkpixels(prob_array['H'],ans_array[str(i)])
                if m > self.getFigureDarkpixels(prob_array['G'],prob_array['H']):
                    max_list.append(m)
                    i +=1 
                    return m
                              
    def getFigureDarkpixels(self, figArray, figArray2):
        # in 'L', 255 is white
        white1 = np.count_nonzero(figArray)
        black1 = figArray.size - white1
        white2 = np.count_nonzero(figArray2)
        black2 = figArray2.size - white2
        difference = abs(black2 - black1)
        return difference     
                    
                    
    def image_combo(self, prob_fig, prob_array):
        AB = self.centerImageArray(np.array(ImageChops.darker(prob_fig['A'],prob_fig['B'])))
        BC = self.centerImageArray(np.array(ImageChops.darker(prob_fig['B'],prob_fig['C'])))
        AC = self.centerImageArray(np.array(ImageChops.darker(prob_fig['A'],prob_fig['C'])))
       
        ABisC = self.getFigureDarkpixels(AB, prob_array['C'])
        BCisA = self.getFigureDarkpixels(BC, prob_array['A'])
        ACisB = self.getFigureDarkpixels(AC, prob_array['B'])
        
        
        min_list = [ABisC,BCisA,ACisB]
        print(min_list)
        min_value = min(min_list)
        min_index = np.argmin(min_list)
        m = [min_value, min_index]
        return m
               
    def ans_combo(self, ans_fig, ans_array, prob_fig,prob_array,min_index):
        
        GH = self.centerImageArray(np.array(ImageChops.darker(prob_fig['G'],prob_fig['H'])))
        
        HI = [self.centerImageArray(np.array(ImageChops.darker(prob_fig['H'],ans_fig[str(x)]))) for x in range(1,9)]
        GI = [self.centerImageArray(np.array(ImageChops.darker(prob_fig['G'],ans_fig[str(x)]))) for x in range(1,9)]
                   
        
        if min_index == 0:
            GHlist = [self.compare_images(GH, ans_array[str(x)]) for x in range(1,9)]
            GH_index = np.argmin(GHlist)
            GHpixel = [self.getFigureDarkpixels(GH, ans_array[str(x)]) for x in range(1,9)]
            GHpix_index = np.argmin(GHpixel)
            if min(GHlist)== 0:
                answer1 = GH_index + 1
                print(answer1)
                return answer1
            elif min(GHpixel) == 0:
                answer2 = GHpix_index + 1
                print(answer2)
                return answer2
            elif min(GHlist) != 0 and min(GHpixel) != 0:
                answer1 = GH_index + 1
                answer2 = GHpix_index + 1
                answers = [answer1,answer2]
                return random.choice(answers)

        elif min_index == 1:
            HIlist = [self.compare_images(HI[x], prob_array['G']) for x in range(1,9)]
            HI_index = np.argmin(HIlist)
            HIpixel = [self.getFigureDarkpixels(HI[x], prob_array['G']) for x in range(1,9)]
            HIpix_index = np.argmin(GHpixel)            
            if min(HIlist)== 0:
                answer1 = HI_index + 1
                print(answer1)
                return answer1
            elif min(HIpixel) == 0:
                answer2 = HIpix_index + 1
                print(answer2)
                return answer2
            elif min(HIlist) != 0 and min(HIpixel) != 0:
                answer1 = HI_index + 1
                answer2 = HIpix_index + 1 
                answers = [answer1,answer2]
                return random.choice(answers)
      
        elif min_index == 2:
            GIlist = [self.compare_images(GI[x], prob_array['H']) for x in range(1,9)]
            GI_index = np.argmin(GIlist)
            GIpixel = [self.getFigureDarkpixels(GI[x], prob_array['H']) for x in range(1,9)]
            GIpix_index = np.argmin(GIpixel) 
            if min(GIlist)== 0:
                answer1 = GI_index + 1
                print(answer1)
                return answer1
            elif min(GIpixel) == 0:
                answer2 = GIpix_index + 1
                print(answer2)
                return answer2
            elif min(GIlist) != 0 and min(GIpixel) != 0:
                answer1 = GI_index + 1
                answer2 = GIpix_index + 1   
                answers = [answer1,answer2]
                return random.choice(answers)            
                           
                
    def image_difference(self, prob_fig, prob_array, ans_fig, ans_array):
        
        diffAB= ImageChops.difference(prob_fig['A'], prob_fig['B'])
        diffarrayAB = self.centerImageArray(np.array(diffAB))
        diffGH = ImageChops.difference(prob_fig['G'], prob_fig['H'])
        diffarrayGH = self.centerImageArray(np.array(diffGH))
        diffAD= ImageChops.difference(prob_fig['A'], prob_fig['D'])
        diffarrayAD = self.centerImageArray(np.array(diffAD))
        diffBE = ImageChops.difference(prob_fig['B'], prob_fig['E'])
        diffarrayBE = self.centerImageArray(np.array(diffBE))
        diffDG = ImageChops.difference(prob_fig['D'], prob_fig['G'])
        diffarrayDG = self.centerImageArray(np.array(diffDG))
        diffEH = ImageChops.difference(prob_fig['E'], prob_fig['H'])
        diffarrayEH = self.centerImageArray(np.array(diffEH))        
        
    def make_transparent(self,img):
        
        pixdata = img.load()
    
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)
        
        
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
