import random


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().

    # . The constructor will be called at the beginning of the program, so you may
    #  use this method to initialize any information necessary before your agent begins
    #  solving problems.
    def __init__(self):
        pass
    
    SIZE={
            "very small" :1,
            "small" :2,
            "medium" :3,
            "large" :4,
            "very large" :5,
            "huge" :6,
    }
    
    TRANSFORMATION_SCORE_DICT = {
    "align" :18,
    "angle" : 10,
    "delete" : 100,
    "fill" : 20,
    "height" : 25,
    "reflection": 8,
    "shape" : 8,
    "size" : 25,
    "width": 25,
    "unchanged": 1,
    "same_length" : 15,
    } 
    
    POSITION_SCORE_DICT = {
    "left-of" : 20,
    "overlaps" : 10,
    "above" : 10,
    }
    
    
    def Solve(self, problem):
        
        
        one = problem.figures['1']
        two = problem.figures['2']
        three = problem.figures['3']
        four = problem.figures['4']
        five = problem.figures['5']
        six = problem.figures['6']

        a = problem.figures['A']
        b = problem.figures['B']
        c = problem.figures['C']
      

        maxscore = 0   
        answer = -1
        
        
        dictForObjsMatched = {} # dictionary to match objects

        ATTR_SCORE_DICT = {
               "fill": 3,
               "size": 2,
               "width": 2,
               "height": 2,
               "alignment" :7,
               "angle": 3,
               "shape": 2,
               "left-of": 2,
               "inside" : 2,
               "above" : 5,
       
       }
        
        
        if problem.problemType == "2x2":


            dictForObjsMatched = self.match_objects(a, b, dictForObjsMatched, ATTR_SCORE_DICT)
            dictForObjsMatched = self.match_objects(a, c, dictForObjsMatched, ATTR_SCORE_DICT)
            for x in range(1,7):
                ans = problem.figures[str(x)]
                dictForObjsMatched = self.match_objects(b, ans, dictForObjsMatched, ATTR_SCORE_DICT)
                dictForObjsMatched = self.match_objects(c, ans, dictForObjsMatched, ATTR_SCORE_DICT)
    
            print("\n" + problem.name + "\n")
    
            transformDict = {}  # create dictionary for transformations
    
            self.obj_a_comparison(a, b, 'ab', transformDict, dictForObjsMatched)
    
            self.obj_a_comparison(a, c, 'ac', transformDict, dictForObjsMatched)
    
            for x in range(1, 7):     
    
                d = problem.figures[str(x)]
    
                print('\n  Now comparing answer: ' + str(x) + ' to ' + problem.name + ':\n')
    
                score = 0  
    
    
                score = self.delete_transformation(a, b, c, d, 'ab', 'cd', problem, score, transformDict, x)
    
                score = self.delete_transformation(a, c, b,  d, 'ac', 'bd', problem, score, transformDict, x)
    
    
                score = self.obj_answer_comparison(c, problem, x, 'ab', 'cd',score, transformDict, dictForObjsMatched)
    
                score = self.obj_answer_comparison(b, problem, x, 'ac', 'bd', score, transformDict, dictForObjsMatched)
    
    
    
                objCompareList = [b, c]
                score = self.unchanged_transformation(dictForObjsMatched, ATTR_SCORE_DICT, objCompareList, problem,score, x)
    
                
                if score > maxscore:
                    maxscore = score
                    answer = x

                elif score == maxscore: 
                    if random.randint(0,1) == 1:
                        maxscore = score
                        answer = x
        
            return answer 


        if problem.problemType == "3x3":
            
            one = problem.figures['1']
            two = problem.figures['2']
            three = problem.figures['3']
            four = problem.figures['4']
            five = problem.figures['5']
            six = problem.figures['6']
            seven = problem.figures['7']
            eight = problem.figures['8']
    
            a = problem.figures['A']
            b = problem.figures['B']
            c = problem.figures['C']
            d = problem.figures['D']
            e = problem.figures['E']
            f = problem.figures['F']
            g = problem.figures['G']
            h = problem.figures['H']               
            
            transformDict = {}  # create dictionary for transformations

            dictForObjsMatched = self.match_objects(a, c, dictForObjsMatched, ATTR_SCORE_DICT)

            dictForObjsMatched = self.match_objects(a, g, dictForObjsMatched, ATTR_SCORE_DICT)
            
            horList = [a,b,b,c,d,e,e,f,g,h]
            i = 0
            j = 1
            while j < 11:
                dictForObjsMatched = self.match_objects(horList[i],horList[j], dictForObjsMatched, ATTR_SCORE_DICT)
                i += 2
                j +=2

            vertList = [a,d,d,g,b,e,e,h,c,f]
            k = 0
            l = 1
            while l < 11:      
                dictForObjsMatched = self.match_objects(vertList[k],vertList[l], dictForObjsMatched, ATTR_SCORE_DICT)
                k += 2
                l += 2           
                
            diagList = [c,g,c,e,e,g,a,e]
            m = 0
            n = 1
            while n < 9:
                dictForObjsMatched = self.match_objects(diagList[m], diagList[n], dictForObjsMatched, ATTR_SCORE_DICT)
                m += 2
                n +=2            
            
            
            figureList = [a,b,c,d,e,f,g,h]
                
            for x in range(1,9):
                ans = problem.figures[str(x)]
                i = 0
                listToCompare = [c,g,f,h,a,e]
                while i < len(listToCompare):
                    dictForObjsMatched = self.match_objects(listToCompare[i], ans, dictForObjsMatched, ATTR_SCORE_DICT)
                    i +=1
                
            print("\n" + problem.name + "\n")
                  

            horizontalCompare = [a,c,a,b,b,c,d,e,e,f,g,h]
            verticalCompare = [a,g,a,d,d,g,b,e,e,h,c,f]
            diagonalCompare = [c,g,c,e,e,g,a,e]
            horStr = ['ac','ab','bc','de','ef','gh']
            vertStr = ['ag','ad','dg','be','eh','cf']
            diagStr = ['cg','ce','eg','ae']
            s = 0
            t = 1
            while s < len(horizontalCompare) and t < len(horizontalCompare) and s < len(horStr):
                self.obj_a_comparison(horizontalCompare[s], horizontalCompare[t], horStr[s], transformDict, dictForObjsMatched)
                self.obj_a_comparison(verticalCompare[s], verticalCompare[t], vertStr[s], transformDict, dictForObjsMatched)
                s += 2
                t += 2
            
            s = 0
            t = 1
            while s < len(diagonalCompare) and t < len(diagonalCompare) and s < len(diagStr):
                self.obj_a_comparison(diagonalCompare[s], diagonalCompare[t], diagStr[s], transformDict, dictForObjsMatched)
                s += 2
                t += 2
                
            for x in range(1, 9):     
                i = problem.figures[str(x)]

                print('\n  Now comparing answer: ' + str(x) + ' to ' + problem.name + ':\n')
                score = 0  

            
                dL1 = [a,e,a,e]
                dL2 = [c,f,g,h]
                dL3 = [g,h,c,f]
                dL4 = [i,i,i,i]
                dVar1 = ['ac','ef','ag','eh']
                dVar2 = ['gi','hi','ci','fi']
                j = 0
                while j <len(dL1):
                    score = self.delete_transformation(dL1[j], dL2[j], dL3[j], dL4[j], dVar1[j],dVar2[j], problem, score, transformDict, x)
                    j +=1
            
                
                answerCompList = [g,h,h,c,f,f,a,e]
                varComp = ['ac','bc','gh','ag','dg','cf','cg','ae']
                varComp1 = ['gi','hi','hi','ci','fi','fi','ai','ei']
                j = 0
                while j < len(answerCompList):
                    score = self.obj_answer_comparison(answerCompList[j], problem, x, varComp[j],varComp1[j],  
                                                      score, transformDict, dictForObjsMatched) 
                    j +=1
                    
                
                objCompareList = [a, c, f, g, h]
                
                score = self.unchanged_transformation(dictForObjsMatched, ATTR_SCORE_DICT, objCompareList, problem, score, x)

                
                
                
                if score > maxscore:
                    maxscore = score
                    answer = x
                elif score == maxscore: 
                    if random.randint(0,1) == 0:
                        maxscore = score  
                        answer = x

            return answer
        

    def match_objects(self, ravensFig1, ravensFig2, dictForObjsMatched, ATTR_SCORE_DICT):

        

        candidateObjsList = [] # candidate object of ravensFig2 list, will be removed once matched

        matchObjsList = []

        if len(ravensFig2.objects) >= len(ravensFig1.objects):

            for key2 in sorted(ravensFig2.objects):
                candidateObjsList.append(ravensFig2.objects[key2])

            for key1 in sorted(ravensFig1.objects):
                obj1 = ravensFig1.objects[key1]
                objTotal = None
                maxscore = 0
                for obj2 in candidateObjsList:
                    score = 0
      
                    for n in range(len(ATTR_SCORE_DICT)):
                        attributeKeys = list(ATTR_SCORE_DICT.keys())
                        attributeName = attributeKeys[n]
                        attributeValues = list(ATTR_SCORE_DICT.values())
                        schange = attributeValues[n]
                            
                        if attributeName in obj1.attributes and attributeName in obj2.attributes:
                            if obj1.attributes[attributeName] == obj2.attributes[attributeName]:
                                score += schange
                                    

                    if score > maxscore:
                        maxscore = score
                        objTotal = obj2
                        

                if objTotal is not None:
                    matchObjsList.append((obj1.name, objTotal.name))
                    candidateObjsList.remove(objTotal)

        elif len(ravensFig2.objects) < len(ravensFig1.objects):

            for key1 in sorted(ravensFig1.objects):
                candidateObjsList.append(ravensFig1.objects[key1])

            for key2 in sorted(ravensFig2.objects):
                obj2 = ravensFig2.objects[key2]
                objTotal = None
                maxscore = 0
                for obj1 in candidateObjsList:
                    score = 0
                   
                    for n in range(len(ATTR_SCORE_DICT.keys())):                        
                        attributeKeys = list(ATTR_SCORE_DICT.keys())
                        attributeName = attributeKeys[n]
                        attributeValues = list(ATTR_SCORE_DICT.values())
                        schange = attributeValues[n]
                        if attributeName in obj1.attributes and attributeName in obj2.attributes:
                            if obj1.attributes[attributeName] == obj2.attributes[attributeName]:
                                score += schange
                                    
                  
                    if score > maxscore:
                        maxscore = score
                        objTotal = obj1
                       

                if objTotal is not None:
                    matchObjsList.append((objTotal.name, obj2.name))
                    candidateObjsList.remove(objTotal)

        dictForObjsMatched[str(ravensFig1.name) + ', ' +str(ravensFig2.name)] = matchObjsList

        return dictForObjsMatched
    
    def delete_transformation(self, a, b, c, ans, figPairs, figPairs1, problem, score, transformDict, x):

        alength = len(a.objects)
        blength = len(b.objects)
        clength = len(c.objects)
        answerlength = len(problem.figures[str(x)].objects)

        transformDict[figPairs + 'diffDelete'] = alength - blength
        transformDict[figPairs1 + 'diffDelete'] = clength - answerlength

        if transformDict[figPairs + 'diffDelete'] == transformDict[figPairs1 + 'diffDelete'] and transformDict[figPairs + 'diffDelete'] != 0:
            
            score += (Agent.TRANSFORMATION_SCORE_DICT['delete'] * abs(transformDict[figPairs + 'diffDelete']))
            
        elif transformDict[figPairs + 'diffDelete'] == transformDict[figPairs1 + 'diffDelete'] and transformDict[figPairs + 'diffDelete'] == 0:
            score += Agent.TRANSFORMATION_SCORE_DICT['delete']
            
        else: 
            if alength != 0 and blength != 0 and clength != 0 and answerlength != 0:
                transformDict[figPairs + 'diffDeleteFunction'] = float(blength)/alength
                transformDict[figPairs1 + 'diffDeleteFunction'] = float(answerlength)/clength
                if transformDict[figPairs + 'diffDeleteFunction'] == transformDict[figPairs1 + 'diffDeleteFunction']:
                    score += Agent.TRANSFORMATION_SCORE_DICT['delete'] * 2
        return score

    def unchanged_transformation(self, dictForObjsMatched, ATTR_SCORE_DICT, objCompareList, problem, score, x):

        ansObj = problem.figures[str(x)]
        

        for c in objCompareList:
            for n in range(len(dictForObjsMatched[str(c.name) + ', ' + str(x)])):
                cObjName, ansObjName = dictForObjsMatched[str(c.name) + ', ' +str(x)][n][0], dictForObjsMatched[str(c.name) + ', ' +str(x)][n][1]
                cObj, ansObj = c.objects[str(cObjName)], problem.figures[str(x)].objects[str(ansObjName)]

                for n in range(len(ATTR_SCORE_DICT)):
                    attributeKeys = list(ATTR_SCORE_DICT.keys())
                    attributeName = attributeKeys[n]
                    if attributeName in cObj.attributes and attributeName in ansObj.attributes:
                        if ansObj.attributes[attributeName] == cObj.attributes[attributeName]:
                            score += Agent.TRANSFORMATION_SCORE_DICT['unchanged']
                            
        return score    
    
    def transformation_calculation(self, score, transformDict, attribute, transformScores):
        attributeName = attribute.title()
        if attributeName in transformDict and attributeName in transformDict:
            if (transformDict[attributeName]) == (transformDict[attributeName]):
                score += transformScores
        return score    

    def obj_a_comparison(self, a, b, figPairs, transformDict, dictForObjsMatched):

        
        for n in range(len(dictForObjsMatched[str(a.name) + ', ' + str(b.name)])):
            keya, keyb = dictForObjsMatched[str(a.name) + ', ' + str(b.name)][n][0], dictForObjsMatched[str(a.name) + ', ' +str(b.name)][n][1]
            aObj, bObj = a.objects[str(keya)], b.objects[str(keyb)]

            
            self.height_width_comparison(aObj, bObj, transformDict,figPairs, n)

            
            transformDict[str(n) + figPairs + 'diffShape'] = (aObj.attributes['shape'] + '-' + bObj.attributes['shape'])
            
            i = 0
            while i < len(Agent.POSITION_SCORE_DICT):
                positionKeys = list(Agent.POSITION_SCORE_DICT.keys())
                self.attribute_comparison(aObj, bObj,transformDict, positionKeys[i], figPairs, n)
                i += 1
            

            self.attribute_comparison(aObj, bObj,transformDict,'size', figPairs, n)

            
            if 'alignment' in aObj.attributes and 'alignment' in bObj.attributes:
                if aObj.attributes['alignment'] != bObj.attributes['alignment']:
                    transformDict[str(n) + figPairs + 'diffAlign'] = aObj.attributes['alignment'] + '-' + bObj.attributes['alignment']
                    
            
            if aObj.attributes['fill'] == bObj.attributes['fill']:
                transformDict[str(n) + figPairs + 'diffFill'] = 0
            elif aObj.attributes['fill'] ==  True and bObj.attributes['fill'] == False:
                transformDict[str(n) + figPairs + 'diffFill'] = -1  
            elif aObj.attributes['fill'] == False and bObj.attributes['fill'] == True:
                transformDict[str(n) + figPairs + 'diffFill'] = 1  

        
            if 'angle' in aObj.attributes and 'angle' in bObj.attributes: 
                transformDict[str(n) + figPairs + 'diffAngle'] = int(aObj.attributes['angle']) - int(bObj.attributes['angle'])
                
            if len(a.objects) == len(b.objects):
                transformDict[str(n) + figPairs + 'same_length'] = True
            

    def obj_answer_comparison(self, c, problem, x, figPairs, figPairs1,
                        score, transformDict, dictForObjsMatched):

        ansObjFigure = problem.figures[str(x)]
        
        for n in range(len(dictForObjsMatched[str(c.name) + ', ' + str(x)])):
            keyc, keyans = dictForObjsMatched[str(c.name) + ', ' + str(x)][n][0], dictForObjsMatched[str(c.name) + ', ' +str(x)][n][1]
            cObj, ansObj = c.objects[str(keyc)], ansObjFigure.objects[keyans]

            i = 0
            while i < len(Agent.POSITION_SCORE_DICT):
                positionKeys = list(Agent.POSITION_SCORE_DICT.keys())
                positionValues = list(Agent.POSITION_SCORE_DICT.values())
                self.attribute_comparison(cObj, ansObj,transformDict,positionKeys[i], figPairs, n)
                score = Agent.transformation_calculation(self, score, transformDict, positionKeys[i], positionValues[i])
                i +=1
            
            
            
            self.height_width_comparison(cObj, ansObj,transformDict, figPairs, n)

            score = Agent.transformation_calculation(self, score, transformDict, 'height', Agent.TRANSFORMATION_SCORE_DICT['height'])
            score = Agent.transformation_calculation(self,score, transformDict,'width', Agent.TRANSFORMATION_SCORE_DICT['width'])
            score = Agent.transformation_calculation(self, score, transformDict,'size', Agent.TRANSFORMATION_SCORE_DICT['size'])

            transformDict[str(n) + figPairs1 + 'diffShape'] = (cObj.attributes['shape'] + '-' + ansObj.attributes['shape'])
            
            if str(n) + figPairs + 'diffShape' in transformDict and str(n) + figPairs1 + 'diffShape' in transformDict:
                if (transformDict[str(n) + figPairs + 'diffShape']) == (transformDict[str(n) + figPairs1 + 'diffShape']):
                    score += Agent.TRANSFORMATION_SCORE_DICT['shape']
            
            
            ansValue = ansObj.attributes['fill']
            if cObj.attributes['fill'] == ansValue:
                transformDict[str(n) + figPairs1 + 'diffFill'] = 0
            else:
                transformDict[str(n) + figPairs1 + 'diffFill'] = 1
                
            if str(n) + figPairs + 'diffFill' in transformDict and str(n) + figPairs1 + 'diffFill' in transformDict:
                if transformDict[str(n) + figPairs + 'diffFill'] == transformDict[str(n) + figPairs1 + 'diffFill']:
                    score += Agent.TRANSFORMATION_SCORE_DICT['fill']
               
            
            if 'alignment' in cObj.attributes and 'alignment' in ansObj.attributes:
                if cObj.attributes['alignment'] != ansObj.attributes['alignment']:
                    transformDict[str(n) + figPairs1 + 'diffAlign'] = cObj.attributes['alignment'] + '-' + ansObj.attributes['alignment']
                    
                if (str(n) + figPairs + 'diffAlign') in transformDict and (str(n) + figPairs1 + 'diffAlign') in transformDict:
                    if (transformDict[str(n) + figPairs + 'diffAlign']) == (transformDict[str(n) + figPairs1 + 'diffAlign']) and transformDict[
                        str(n) + figPairs + 'diffAlign'] != None and transformDict[str(n) + figPairs1 + 'diffAlign'] != None:
                        score += Agent.TRANSFORMATION_SCORE_DICT['align']
                  
            
            if 'angle' in cObj.attributes and 'angle' in ansObj.attributes:  
                transformDict[str(n) + figPairs1 + 'diffAngle'] = int(cObj.attributes['angle']) - int(ansObj.attributes['angle'])
                
            if str(n) + figPairs + 'diffAngle' in transformDict and str(n) + figPairs1 + 'diffAngle' in transformDict:
                if abs(transformDict[str(n) + figPairs + 'diffAngle'] + 180) % 360 == abs(transformDict[str(n) + figPairs1 + 'diffAngle']):
                    score += Agent.TRANSFORMATION_SCORE_DICT['reflection']
         
                elif transformDict[str(n) + figPairs + 'diffAngle'] == transformDict[str(n) + figPairs1 + 'diffAngle']:
                    score += Agent.TRANSFORMATION_SCORE_DICT['angle']
                    
            if len(c.objects) == len(ansObjFigure.objects):
                transformDict[str(n) + figPairs1 + 'same_length'] = True
            
            if (str(n) + figPairs + 'same_length') in transformDict and (str(n) + figPairs1 + 'same_length') in transformDict:
                if (transformDict[str(n) + figPairs + 'same_length']) == (transformDict[str(n) + figPairs1 + 'same_length']) and transformDict[
                    str(n) + figPairs + 'same_length'] == True and transformDict[str(n) + figPairs1 + 'same_length'] == True:
                    score += Agent.TRANSFORMATION_SCORE_DICT['same_length']            
                 
        return score

    def attribute_comparison(self, aObj, bObj, transformDict, attribute, figPairs, n):
        attributeName = attribute.title()
        if attribute == 'size' or attribute == 'width' or attribute == 'height':
            if attribute in aObj.attributes and attribute in bObj.attributes:
                transformDict[str(n) + figPairs + attributeName + 'diff'] = self.SIZE[aObj.attributes[
                    attribute]] - self.SIZE[bObj.attributes[attribute]]
              
        else:
            if attribute in aObj.attributes and attribute in bObj.attributes:
                transformDict[str(n) + figPairs + attributeName + 'Diff'] = ( aObj.attributes[
                    attribute]) + ( bObj.attributes[attribute])
              

    def height_width_comparison(self, aObj, bObj,transformDict, figPairs , n):
        
        if aObj.attributes['shape'] == 'square' and 'height' not in aObj.attributes and 'width' not in aObj.attributes:
            aObj.attributes['height'] = aObj.attributes['size']
            aObj.attributes['width'] = aObj.attributes['size'] 
        
        if bObj.attributes['shape'] == 'square' and 'height' not in bObj.attributes and 'width' not in bObj.attributes:
            bObj.attributes['height'] = bObj.attributes['size']
            bObj.attributes['width'] = bObj.attributes['size']        
            
        if 'height' in aObj.attributes and 'height' in bObj.attributes:
            transformDict[str(n) + figPairs + 'diffHeight'] = Agent.SIZE[aObj.attributes['height']] 
            - Agent.SIZE[bObj.attributes['height']]
            
        if 'width' in aObj.attributes and 'width' in bObj.attributes:
            transformDict[str(n) + figPairs + 'diffWidth'] = Agent.SIZE[aObj.attributes['width']] 
            - Agent.SIZE[bObj.attributes['width']]
            
    
        
            

    

    
        

    
