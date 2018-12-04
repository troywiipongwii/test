from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageDraw
import numpy as np
import math

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    votes = {}

    # Constant values for weighted voting
    diffVote = 1
    flipVote = 5
    mirrorVote = 5
    identicalVote = 11
    increasingVote = 13 #3x3
    decreasingVote = 13 #3x3
    alternatingVote = 13 #3x3
    orVote = 13 #3x3
    norVote = 13 #3x3
    subtractVote = 13 #3x3
    andVote = 13 #3x3
    xorVote = 13 #3x3
    orVote = 13 #3x3
    diffTestVote = 13
    patternVote = 20
    sameDiagonalVote = 20
    topSplitVote = 20
    
    def Solve(self, problem):
    
        # Determine existing relational ratios. Relationships from the first to last figures also seem to matter

        A = Image.open("A.png").convert("L")
        B = Image.open("B.png").convert("L")
        C = Image.open("C.png").convert("L")
        D = Image.open("D.png").convert("L")
        E = Image.open("E.png").convert("L")
        F = Image.open("F.png").convert("L")
        G = Image.open("G.png").convert("L")
        H = Image.open("H.png").convert("L")
    
        one = Image.open("1.png").convert("L")
        two = Image.open("2.png").convert("L")
        three = Image.open("3.png").convert("L")
        four = Image.open("4.png").convert("L")
        five = Image.open("5.png").convert("L")
        six = Image.open("6.png").convert("L")
        seven = Image.open("7.png").convert("L")
        eight = Image.open("8.png").convert("L")
    
        ravensFigures = ['A','B','C','D','E','F','G','H']
    
        solFigures = ['one','two','three','four','five','six','seven','eight']
    
    
        RavDict = {}
        SolDict = {}
        
        i = 0
        while i < len(ravensFigures):
            new_array = 'array{}'.format(ravensFigures[i])
            sol_array = 'array{}'.format(solFigures[i])
            create_rav_array = np.array(ravensFigures[i])
            create_sol_array = np.array(solFigures[i])
            RavDict[new_array] = create_rav_array
            SolDict[sol_array] = create_sol_array 
            i += 1
    
        
        #Horizontal
        #abc
        abPixelRatio = self.getRatioDarkPixelsQuads(aArray, bArray)
        bcPixelRatio = self.getRatioDarkPixelsQuads(bArray, cArray)
        acPixelRatio = self.getRatioDarkPixelsQuads(aArray, cArray)

        #def
        dePixelRatio = self.getRatioDarkPixelsQuads(dArray, eArray)
        efPixelRatio = self.getRatioDarkPixelsQuads(eArray, fArray)
        dfPixelRatio = self.getRatioDarkPixelsQuads(dArray, fArray)

        #gh?
        ghPixelRatio = self.getRatioDarkPixelsQuads(gArray, hArray)

        #Vertical
        #adg
        adPixelRatio = self.getRatioDarkPixelsQuads(aArray, dArray)
        dgPixelRatio = self.getRatioDarkPixelsQuads(dArray, gArray)
        agPixelRatio = self.getRatioDarkPixelsQuads(aArray, gArray)

        #beh
        bePixelRatio = self.getRatioDarkPixelsQuads(bArray, eArray)
        ehPixelRatio = self.getRatioDarkPixelsQuads(eArray, hArray)
        bhPixelRatio = self.getRatioDarkPixelsQuads(bArray, hArray)

        #cf?
        cfPixelRatio = self.getRatioDarkPixelsQuads(cArray, gArray)

        #Diagonal
        #ceg
        cePixelRatio = self.getRatioDarkPixelsQuads(cArray, eArray)
        egPixelRatio = self.getRatioDarkPixelsQuads(eArray, gArray)
        cgPixelRatio = self.getRatioDarkPixelsQuads(cArray, gArray)

        #ae?
        aePixelRatio = self.getRatioDarkPixelsQuads(aArray, eArray)

        solImageArrays = {}
        solHorizRatios = {}
        solHorizRatiosFirstLast = {}
        solVertRatios = {}
        solVertRatiosFirstLast = {}
        solDiagRatios = {}
        solDiagRatioFirstLast = {}
        solutionNames = []
        # Collect ratios to possible solutions
        for solName in sorted(problem.figures):
            if solName.isnumeric():
                solArray = self.getImageArray(problem, solName)
                solHorizRatios[solName] = self.getRatioDarkPixelsQuads(hArray, solArray)
                solHorizRatiosFirstLast[solName] = self.getRatioDarkPixelsQuads(gArray, solArray)
                solVertRatios[solName] = self.getRatioDarkPixelsQuads(fArray, solArray)
                solVertRatiosFirstLast[solName] = self.getRatioDarkPixelsQuads(cArray, solArray)
                solDiagRatios[solName] = self.getRatioDarkPixelsQuads(eArray, solArray)
                solDiagRatioFirstLast[solName] = self.getRatioDarkPixelsQuads(aArray, solArray)
                solutionNames.append(solName)
                solImageArrays[solName] = solArray

        # Determine best horizontal ratios.
        self.getClosest3x3Ratio(abPixelRatio, bcPixelRatio, ghPixelRatio, solHorizRatios)
        self.getClosest3x3Ratio(dePixelRatio, efPixelRatio, ghPixelRatio, solHorizRatios)
        #try
        self.getClosestRatio(solHorizRatiosFirstLast, acPixelRatio)
        self.getClosestRatio(solHorizRatiosFirstLast, dfPixelRatio)

        #vertical
        self.getClosest3x3Ratio(adPixelRatio, dgPixelRatio, cfPixelRatio, solVertRatios)
        self.getClosest3x3Ratio(bePixelRatio, ehPixelRatio, cfPixelRatio, solVertRatios)
        self.getClosestRatio(solVertRatiosFirstLast, agPixelRatio)
        self.getClosestRatio(solVertRatiosFirstLast, bhPixelRatio)

        #diagonal
        self.getClosest3x3Ratio(cePixelRatio, egPixelRatio, aePixelRatio, solDiagRatios)
        self.getClosestRatio(solDiagRatioFirstLast, cgPixelRatio)

        #IsSame
        a = self.centerImageArray(aArray)
        b = self.centerImageArray(bArray)
        c = self.centerImageArray(cArray)
        d = self.centerImageArray(dArray)
        e = self.centerImageArray(eArray)
        f = self.centerImageArray(fArray)
        g = self.centerImageArray(gArray)
        h = self.centerImageArray(hArray)
        # horizontal
        if self.isSameFigure(a, b) and self.isSameFigure(b, c):
            if self.isSameFigure(d, e) and self.isSameFigure(e, f):
                for sol in solutionNames:
                    if self.isSameFigure(g, h) and self.isSameFigure(h, self.centerImageArray(solImageArrays[sol])):
                        self.vote(sol, self.identicalVote)
        # vertical
        if self.isSameFigure(a, d) and self.isSameFigure(d, g):
            if self.isSameFigure(b, e) and self.isSameFigure(e, h):
                for sol in solutionNames:
                    if self.isSameFigure(c,f) and self.isSameFigure(f, self.centerImageArray(solImageArrays[sol])):
                        self.vote(sol, self.identicalVote)

        #Test increasing horizontal
        if self.is3x3RelationIncreasing(problem, 'A', 'B', 'C') and self.is3x3RelationIncreasing(problem, 'D', 'E', 'F'):
            for solName in solutionNames:
                if self.is3x3RelationIncreasing(problem, 'G', 'H', solName):
                    self.vote(solName, self.increasingVote)

        #Test increasing vertical
        if self.is3x3RelationIncreasing(problem, 'A', 'D', 'G') and self.is3x3RelationIncreasing(problem, 'B', 'E', 'H'):
            for solName in solutionNames:
                if self.is3x3RelationIncreasing(problem, 'C', 'F', solName):
                    self.vote(solName, self.increasingVote)

        #Test increasing diagonal
        if self.is3x3RelationIncreasing(problem, 'C', 'E', 'G'):
            for solName in solutionNames:
                if self.is3x3RelationIncreasing(problem, 'A', 'E', solName):
                    self.vote(solName, self.increasingVote)

        #Test decreasing horizontal
        if self.is3x3RelationDecreasing(problem, 'A', 'B', 'C') and self.is3x3RelationDecreasing(problem, 'D', 'E', 'F'):
            for solName in solutionNames:
                if self.is3x3RelationDecreasing(problem, 'G', 'H', solName):
                    self.vote(solName, self.decreasingVote)

        #Test decreasing vertical
        if self.is3x3RelationDecreasing(problem, 'A', 'D', 'G') and self.is3x3RelationDecreasing(problem, 'B', 'E', 'H'):
            for solName in solutionNames:
                if self.is3x3RelationDecreasing(problem, 'C', 'F', solName):
                    self.vote(solName, self.decreasingVote)

        #Test decreasing diagonal
        if self.is3x3RelationDecreasing(problem, 'C', 'E', 'G'):
            for solName in solutionNames:
                if self.is3x3RelationDecreasing(problem, 'A', 'E', solName):
                    self.vote(solName, self.increasingVote)

        #Test alternating horizontal
        if self.is3x3Alternating(problem, 'A', 'B', 'C') and self.is3x3Alternating(problem, 'D', 'E', 'F'):
            for solName in solutionNames:
                if self.is3x3Alternating(problem, 'G', 'H', solName):
                    self.vote(solName, self.alternatingVote)

        #Test alternating vertical
        if self.is3x3Alternating(problem, 'A', 'D', 'G') and self.is3x3Alternating(problem, 'B', 'E', 'H'):
            for solName in solutionNames:
                if self.is3x3Alternating(problem, 'C', 'F', solName):
                    self.vote(solName, self.alternatingVote)

        #Test Flips at beginning and end of vert/horizontal/diagonal
        #Horizontal
        if self.isLeftRightFlip(aArray, cArray) and self.isLeftRightFlip(dArray, fArray):
            for solName in solutionNames:
                if self.isLeftRightFlip(gArray, solImageArrays[solName]):
                    self.vote(solName, self.flipVote)

        if self.isUpDownFlip(aArray, cArray) and self.isUpDownFlip(dArray, fArray):
            for solName in solutionNames:
                if self.isUpDownFlip(gArray, solImageArrays[solName]):
                    self.vote(solName, self.flipVote)

        #Vertical
        if self.isLeftRightFlip(aArray, gArray) and self.isLeftRightFlip(bArray, hArray):
            for solName in solutionNames:
                if self.isLeftRightFlip(cArray,solImageArrays[solName]):
                    self.vote(solName, self.flipVote)

        if self.isUpDownFlip(aArray, gArray) and self.isUpDownFlip(bArray, hArray):
            for solName in solutionNames:
                if self.isUpDownFlip(cArray, solImageArrays[solName]):
                    self.vote(solName, self.flipVote)

        #Diagonal
        if self.isLeftRightFlip(cArray, gArray):
            for solName in solutionNames:
                if self.isLeftRightFlip(aArray, solImageArrays[solName]):
                    self.vote(solName, self.flipVote)

        if self.isUpDownFlip(cArray, gArray):
            for solName in solutionNames:
                if self.isUpDownFlip(aArray, solImageArrays[solName]):
                    self.vote(solName, self.flipVote)

        #addTest
        #A or B = C, D or E = F
        if self.addTest(aArray, bArray, cArray):
            if self.addTest(dArray, eArray, fArray):
                for solName in solutionNames:
                    if self.addTest(gArray, hArray, solImageArrays[solName]):
                        self.vote(solName, self.orVote)

        #xorTest
        # vertical
        if self.xorTest(aArray, dArray, gArray):
            if self.xorTest(bArray, eArray, hArray):
                for solName in solutionNames:
                    if self.xorTest(cArray, fArray, solImageArrays[solName]):
                        self.vote(solName, self.xorVote)
        if self.xorTest(aArray, gArray, dArray):
            if self.xorTest(bArray, hArray, eArray):
                for solName in solutionNames:
                    if self.xorTest(cArray, solImageArrays[solName], fArray):
                        self.vote(solName, self.xorVote)
        if self.xorTest(dArray, gArray, aArray):
            if self.xorTest(eArray, hArray, bArray):
                for solName in solutionNames:
                    if self.xorTest(solImageArrays[solName], fArray, cArray):
                        self.vote(solName, self.xorVote)


        # horizontal
        if self.xorTest(aArray, bArray, cArray):
            if self.xorTest(dArray, eArray, fArray):
                for solName in solutionNames:
                    if self.xorTest(gArray, hArray, solImageArrays[solName]):
                        self.vote(solName, self.xorVote)

        if self.xorTest(aArray, cArray, bArray):
            if self.xorTest(dArray, fArray, eArray):
                for solName in solutionNames:
                    if self.xorTest(gArray, solImageArrays[solName], hArray):
                        self.vote(solName, self.xorVote)
        if self.xorTest(bArray, cArray, aArray):
            if self.xorTest(eArray, fArray, dArray):
                for solName in solutionNames:
                    if self.xorTest(solImageArrays[solName], hArray, gArray):
                        self.vote(solName, self.xorVote)

#       #subtractTest
#       #A-B = C , D-E=F
        if self.subtractTest(aArray, bArray, cArray) and self.subtractTest(dArray, eArray, fArray):
            for solName in solutionNames:
                if self.subtractTest(gArray, hArray, solImageArrays[solName]):
                    self.vote(solName, self.subtractVote)

        #A-D=G, B-E=H
        if self.subtractTest(aArray, dArray, gArray) and self.subtractTest(bArray, eArray, hArray):
            for solName in solutionNames:
                if self.subtractTest(cArray, fArray, solImageArrays[solName]):
                    self.vote(solName, self.subtractVote)

        #andTest
        #A^B=C,D^E=F
        if self.andTest(aArray,bArray, cArray) and self.andTest(dArray, eArray, fArray):
            for solName in solutionNames:
                if self.andTest(gArray, hArray, solImageArrays[solName]):
                    self.vote(solName, self.andVote)
        #A^C=B, D^F=E
        if self.andTest(aArray,cArray, bArray) and self.andTest(dArray, fArray, eArray):
            for solName in solutionNames:
                if self.andTest(gArray, solImageArrays[solName], hArray):
                    self.vote(solName, self.andVote)
        #B^C=A,B E^F=D
        if self.andTest(bArray, cArray, aArray) and self.andTest(eArray, fArray, dArray):
            for solName in solutionNames:
                if self.andTest(hArray, solImageArrays[solName], gArray):
                    self.vote(solName, self.andVote)
        #A^D=G,B^E=H
        if self.andTest(aArray, dArray, gArray) and self.andTest(bArray, eArray, hArray):
            for solName in solutionNames:
                if self.andTest(cArray, fArray, solImageArrays[solName]):
                    self.vote(solName, self.andVote)
        #A^G=D,B^H=E
        if self.andTest(aArray, gArray, dArray) and self.andTest(bArray, hArray, eArray):
            for solName in solutionNames:
                if self.andTest(cArray, solImageArrays[solName], fArray):
                    self.vote(solName, self.andVote)
        #D^G=A,E^H=B
        if self.andTest(dArray, gArray, aArray) and self.andTest(eArray, hArray, bArray):
            for solName in solutionNames:
                if self.andTest(fArray, solImageArrays[solName], cArray):
                    self.vote(solName, self.andVote)


        #orTest
        #A or B=C,D or E=F
        if self.orTest(aArray,bArray, cArray) and self.orTest(dArray, eArray, fArray):
            for solName in solutionNames:
                if self.orTest(gArray, hArray, solImageArrays[solName]):
                    self.vote(solName, self.orVote)

        #A or C=B, D or F = E
        if self.orTest(aArray,cArray, bArray) and self.orTest(dArray, fArray, eArray):
            for solName in solutionNames:
                if self.orTest(gArray, solImageArrays[solName], hArray):
                    self.vote(solName, self.orVote)

        #B or C = A, E or F = D
        if self.orTest(bArray, cArray, aArray) and self.orTest(eArray, fArray, dArray):
            for solName in solutionNames:
                if self.orTest(hArray, solImageArrays[solName], gArray):
                    self.vote(solName, self.orVote)

        #A or D=G,B or E=H
        if self.orTest(aArray, dArray, gArray) and self.orTest(bArray, eArray, hArray):
            for solName in solutionNames:
                if self.orTest(cArray, fArray, solImageArrays[solName]):
                    self.vote(solName, self.orVote)

        # A or G = D, B or H = E
        if self.orTest(aArray, gArray, dArray) and self.orTest(bArray, hArray, eArray):
            for solName in solutionNames:
                if self.orTest(cArray, solImageArrays[solName], fArray):
                    self.vote(solName, self.orVote)
        # D or G = A, H or E = B
        if self.orTest(dArray, gArray, aArray) and self.orTest(hArray, eArray, bArray):
            for solName in solutionNames:
                if self.orTest(fArray, solImageArrays[solName], cArray):
                    self.vote(solName, self.orVote)


        #NORTest
        #A or B=C,D or E=F
        if self.norTest(aArray,bArray, cArray) and self.norTest(dArray, eArray, fArray):
            for solName in solutionNames:
                if self.norTest(gArray, hArray, solImageArrays[solName]):
                    self.vote(solName, self.norVote)

        #A or C=B, D or F = E
        if self.norTest(aArray,cArray, bArray) and self.norTest(dArray, fArray, eArray):
            for solName in solutionNames:
                if self.norTest(gArray, solImageArrays[solName], hArray):
                    self.vote(solName, self.norVote)

        #B or C = A, E or F = D
        if self.norTest(bArray, cArray, aArray) and self.norTest(eArray, fArray, dArray):
            for solName in solutionNames:
                if self.norTest(hArray, solImageArrays[solName], gArray):
                    self.vote(solName, self.norVote)

        #A or D=G,B or E=H
        if self.norTest(aArray, dArray, gArray) and self.norTest(bArray, eArray, hArray):
            for solName in solutionNames:
                if self.norTest(cArray, fArray, solImageArrays[solName]):
                    self.vote(solName, self.norVote)

        # A or G = D, B or H = E
        if self.norTest(aArray, gArray, dArray) and self.norTest(bArray, hArray, eArray):
            for solName in solutionNames:
                if self.norTest(cArray, solImageArrays[solName], fArray):
                    self.vote(solName, self.norVote)
        # D or G = A, H or E = B
        if self.norTest(dArray, gArray, aArray) and self.norTest(hArray, eArray, bArray):
            for solName in solutionNames:
                if self.norTest(fArray, solImageArrays[solName], cArray):
                    self.vote(solName, self.norVote)

        # Difference test
        if self.differenceTest(aArray, bArray, cArray):
            if self.differenceTest(dArray, eArray, fArray):
                for solName in solutionNames:
                    if self.differenceTest(gArray, hArray, solImageArrays[solName]):
                        self.vote(solName, self.diffTestVote)

        #TopLeftPattern, TopRightPattern Test
        matchesR = {}
        sol = "-1"
        for solName in solutionNames:
            matchesR[solName] = self.topRightPatternTest(a, b,c, d, e, f, g, h, self.centerImageArray(solImageArrays[solName]))

        sol = min(matchesR, key=matchesR.get)
        if matchesR[sol] != 100:
            self.vote(sol, self.patternVote)
        matches = {}
        for solName in solutionNames:
            matches[solName] = self.topLeftPatternTest(a, b, c, d, e, f, g, h, self.centerImageArray(solImageArrays[solName]))
        sol = min(matches, key=matches.get)
        if matches[sol] != 100:
            self.vote(sol, self.patternVote)

        #sameDiagonalTest
        self.isDiagonalSameTest(aePixelRatio, solDiagRatios)

        #TopBottomSplitTest - First arg is top, second is bottom of solution
        if self.topBottomSplitTest(aArray, bArray, cArray):
            if self.topBottomSplitTest(dArray, eArray, fArray):
                for solName in solutionNames:
                    if self.topBottomSplitTest(gArray, eArray, solImageArrays[solName]):
                        self.vote(solName, self.topSplitVote)
        if self.topBottomSplitTest(aArray, dArray, gArray):
            if self.topBottomSplitTest(bArray, eArray, hArray):
                for solName in solutionNames:
                    if self.topBottomSplitTest(cArray, fArray, solImageArrays[solName]):
                        self.vote(solName, self.topSplitVote)

        # TopBottomSplitTest-swapping tops and bottoms
        if self.topBottomSplitTest(bArray, aArray, cArray):
            if self.topBottomSplitTest(eArray, dArray, fArray):
                for solName in solutionNames:
                    if self.topBottomSplitTest(eArray, gArray, solImageArrays[solName]):
                        self.vote(solName, self.topSplitVote)
        if self.topBottomSplitTest(dArray, aArray, gArray):
            if self.topBottomSplitTest(eArray, bArray, hArray):
                for solName in solutionNames:
                    if self.topBottomSplitTest(fArray, cArray, solImageArrays[solName]):
                        self.vote(solName, self.topSplitVote)

        return self.getMostVotes()

    # Gets a numpy array representing all pixels in the image.
    def getImageArray(self, problem, figName):
        figure = problem.figures[figName]
        figureImage = Image.open(figure.visualFilename).convert("L")

        figureImage = figureImage.filter(ImageFilter.SMOOTH_MORE)

        nparray = np.array(figureImage)

        nparray[nparray >= 128] = 255
        nparray[nparray < 128] = 0

        return nparray

    # RATIOS---------------------------------------------------------------------------------------------------------------------------------

    # 3x3 Gets ratio of dark pixels in entire image
    def getFigureDarkRatio(self, problem, figName):
        nparray = self.getImageArray(problem, figName)
        # in 'L', 255 is white
        white = np.count_nonzero(nparray)
        return (nparray.size - white) / nparray.size

    # Currently unused. Gets ratio of dark pixels in same location in entire figures
    def getRatioDarkPixelsSameLocation(self, problem, figName, solName):
        figArray = self.getImageArray(problem, figName)
        solArray = self.getImageArray(problem, solName)

        # All non-zero elements at the same position in both arrays
        # in 'L', 255 is white
        sameCoordWhite = np.count_nonzero(figArray==solArray)
        return (figArray.size - sameCoordWhite) / figArray.size

    # Get dark pixel ratios of dark pixels in same location in figures, but return results as quadrants
    def getRatioDarkPixelsQuads(self, figArray, solArray):
        # Return a ratio dictionary where quadrant is key

        figHalves = np.vsplit(figArray, 2)
        figQuadsLeft = np.hsplit(figHalves[0], 2)
        figQuadsRight = np.hsplit(figHalves[1], 2)

        solHalves = np.vsplit(solArray, 2)
        solQuadsLeft = np.hsplit(solHalves[0], 2)
        solQuadsRight = np.hsplit(solHalves[1], 2)

        # All non-zero elements at the same position in both arrays
        # in 'L', 255 is white
        sameCoordNW = np.count_nonzero(figQuadsLeft[0]==solQuadsLeft[0])
        sameCoordSW = np.count_nonzero(figQuadsRight[0]==solQuadsRight[0])
        sameCoordNE = np.count_nonzero(figQuadsLeft[1]==solQuadsLeft[1])
        sameCoordSE = np.count_nonzero(figQuadsRight[1]==solQuadsRight[1])

        ratios = {}
        ratios['nw'] = (figQuadsLeft[0].size - sameCoordNW) / figQuadsLeft[0].size
        ratios['sw'] = (figQuadsRight[0].size - sameCoordSW) / figQuadsRight[0].size
        ratios['ne'] = (figQuadsLeft[1].size - sameCoordNE) / figQuadsLeft[1].size
        ratios['se'] = (figQuadsRight[1].size -sameCoordSE) / figQuadsRight[1].size

        return ratios

    # Returns the ratio of dark to light pixels in each quadrant for the specified figure.
    # Useful for comparing changes within the figure itself instead of figure to figure changes.
    def getFigureDarkPixelQuadRatios(self, figArray):

        figHalves = np.vsplit(figArray, 2)
        figQuadsLeft = np.hsplit(figHalves[0], 2)
        figQuadsRight = np.hsplit(figHalves[1], 2)

        # All non-zero elements
        # In 'L', 255 is white
        NWwhite = np.count_nonzero(figQuadsLeft[0])
        SWwhite = np.count_nonzero(figQuadsRight[0])
        NEwhite = np.count_nonzero(figQuadsLeft[1])
        SEwhite = np.count_nonzero(figQuadsRight[1])

        ratios = {}
        ratios['nw'] = (figQuadsLeft[0].size - NWwhite) / figQuadsLeft[0].size
        ratios['sw'] = (figQuadsRight[0].size - SWwhite) / figQuadsRight[0].size
        ratios['ne'] = (figQuadsLeft[1].size - NEwhite) / figQuadsLeft[1].size
        ratios['se'] = (figQuadsRight[1].size - SEwhite) / figQuadsRight[1].size

        return ratios

    # Get the solution quadrants with the closest ratio to the known ratio
    # TODO-It's inconsistent that this is the only ratio method that votes.
    def getClosestRatio(self, solRatios, knownRatio):
        diffNW = {}
        diffNE = {}
        diffSW = {}
        diffSE = {}

        for key, value in sorted(solRatios.items()):
            diffNW[key] = abs(value['nw'] - knownRatio['nw'])
            diffNE[key] = abs(value['ne'] - knownRatio['ne'])
            diffSW[key] = abs(value['sw'] - knownRatio['sw'])
            diffSE[key] = abs(value['se'] - knownRatio['se'])

        # accounting for equivalent values, might be overkill
        leastNW = min(diffNW.values())
        genNW = ((key,value) for (key,value) in  diffNW.items() if value == leastNW)
        nwList = dict(genNW)

        leastNE = min(diffNE.values())
        genNE= ((key,value) for (key,value) in  diffNE.items() if value == leastNE)
        neList = dict(genNE)

        leastSW = min(diffSW.values())
        genSW = ((key,value) for (key,value) in  diffSW.items() if value == leastSW)
        swList = dict(genSW)

        leastSE = min(diffSE.values())
        genSE= ((key,value) for (key,value) in  diffSE.items() if value == leastSE)
        seList = dict(genSE)

        for key, value in nwList.items():
            if key in neList and key in swList and key in seList:
                self.vote(key, self.diffVote)

        for key, value in neList.items():
            if key in nwList and key in swList and key in seList:
                self.vote(key, self.diffVote)

        for key, value in swList.items():
            if key in neList and key in nwList and key in seList:
                self.vote(key, self.diffVote)

        for key, value in seList.items():
            if key in neList and key in swList and key in nwList:
                self.vote(key, self.diffVote)

    # 3x3 requires a different approach. Calculate total ratio across all pairs in relationship
    # Vote for solution that matches most closely
    def getClosest3x3Ratio(self, knownPairRatio1, knownPairRatio2, solRatio1, solRatios):
        # Add matched ratios in knownPair values

        knownNW = knownPairRatio1['nw'] + knownPairRatio2['nw']
        knownNE = knownPairRatio1['ne'] + knownPairRatio2['ne']
        knownSW = knownPairRatio1['sw'] + knownPairRatio2['sw']
        knownSE = knownPairRatio1['se'] + knownPairRatio2['se']

        solNW = {}
        solNE = {}
        solSW = {}
        solSE = {}

        # Add solRatio1 to all solRatios
        for key, value in sorted(solRatios.items()):
            solNW[key] = value['nw'] + solRatio1['nw']
            solNE[key] = value['ne'] + solRatio1['ne']
            solSW[key] = value['sw'] + solRatio1['sw']
            solSE[key] = value['se'] + solRatio1['se']

        diffNW = {}
        diffNE = {}
        diffSW = {}
        diffSE = {}

        for key, value in sorted(solRatios.items()):
            diffNW[key] = abs(value['nw'] - knownNW)
            diffNE[key] = abs(value['ne'] - knownNE)
            diffSW[key] = abs(value['sw'] - knownSW)
            diffSE[key] = abs(value['se'] - knownSE)

        # accounting for equivalent values, might be overkill
        leastNW = min(diffNW.values())
        genNW = ((key,value) for (key,value) in  diffNW.items() if value == leastNW)
        nwList = dict(genNW)

        leastNE = min(diffNE.values())
        genNE= ((key,value) for (key,value) in  diffNE.items() if value == leastNE)
        neList = dict(genNE)

        leastSW = min(diffSW.values())
        genSW = ((key,value) for (key,value) in  diffSW.items() if value == leastSW)
        swList = dict(genSW)

        leastSE = min(diffSE.values())
        genSE= ((key,value) for (key,value) in  diffSE.items() if value == leastSE)
        seList = dict(genSE)

        for key, value in nwList.items():
            if key in neList and key in swList and key in seList:
                self.vote(key, self.diffVote)

        for key, value in neList.items():
            if key in nwList and key in swList and key in seList:
                self.vote(key, self.diffVote)

        for key, value in swList.items():
            if key in neList and key in nwList and key in seList:
                self.vote(key, self.diffVote)

        for key, value in seList.items():
            if key in neList and key in swList and key in nwList:
                self.vote(key, self.diffVote)

    # TESTS - 3x3 Specfic---------------------------------------------------------------------------------------------------------------------------------

    def is3x3RelationIncreasing(self, problem, figName1, figName2, figName3):
        r1 = self.getFigureDarkRatio(problem, figName1)
        r2 = self.getFigureDarkRatio(problem, figName2)
        r3 = self.getFigureDarkRatio(problem, figName3)
        return r3 > r2 > r1

    def is3x3RelationDecreasing(self, problem, figName1, figName2, figName3):
        r1 = self.getFigureDarkRatio(problem, figName1)
        r2 = self.getFigureDarkRatio(problem, figName2)
        r3 = self.getFigureDarkRatio(problem, figName3)
        return r1 > r2 > r3

    # Checking for alternating figure relations, such as A==C, B !=A
    def is3x3Alternating(self, problem, figName1, figName2, figName3):
        f1 = self.getImageArray(problem, figName1)
        f2 = self.getImageArray(problem, figName2)
        f3 = self.getImageArray(problem, figName3)
        return self.isSameFigure(f1, f3) and not self.isSameFigure(f2, f3)

    # C or A = B ..represents overlapping of two images on top of each other to get a figure
    # would I have to test all permutations?...or take the one with more dark pixels and subtract from it?
    # perms would be A or B = C , B or C = A, A or C = B
    def addTest(self, figArray1, figArray2, solArray):
        result = np.add(figArray1, figArray2)

        result[result >= 255] = 255
        result[result < 255] = 0

        img = Image.fromarray(result, mode="L")
        img = ImageOps.invert(img)
        result = np.array(img)
        return self.isSameFigure(result, solArray)

    # A and B and C = C
    def andTest(self, figArray1, figArray2, solArray):
        f1 = Image.fromarray(figArray1, mode="L")
        f2 = Image.fromarray(figArray2, mode="L")

        result = chops.logical_and(f1.convert(mode="1"), f2.convert(mode="1"))

        result = result.convert(mode="L")
        result = np.array(result)

        return self.isSameFigure(result, solArray)

    def orTest(self, figArray1, figArray2, solArray):
        f1 = Image.fromarray(figArray1, mode="L")
        f2 = Image.fromarray(figArray2, mode="L")
        s = Image.fromarray(solArray, mode="L")

        result = chops.logical_or(f1.convert(mode="1"), f2.convert(mode="1"))
        result1 = chops.logical_or(result, s.convert(mode="1"))

        result1 = result1.convert(mode="L")
        result1 = np.array(result1)

        return self.isSameFigure(result1, solArray)

    def norTest(self, figArray1, figArray2, solArray):
        f1 = Image.fromarray(figArray1, mode="L")
        f2 = Image.fromarray(figArray2, mode="L")
        s = Image.fromarray(solArray, mode="L")

        result = chops.logical_or(f1.convert(mode="1"), f2.convert(mode="1"))
        result1 = chops.logical_or(result, s.convert(mode="1"))

        #Invert to negate
        result1 = chops.invert(result1)

        result1 = result1.convert(mode="L")
        result1 = np.array(result1)

        return self.isSameFigure(result1, solArray)


    def xorTest(self, figArray1, figArray2, solArray):
        image1 = Image.fromarray(figArray1, mode="L")
        image2 = Image.fromarray(figArray2, mode="L")

        sol = Image.fromarray(solArray, mode="L")

        result = chops.difference(image1, image2)
        result = np.array(result)

        return self.isSameFigure(result, solArray)

    # A - B = C
    def subtractTest(self, figArray1, figArray2, solArray):
        result = np.subtract(figArray1, figArray2)
        return self.isSameFigure(result, solArray)

    # Is this the same as subtract, or is subtract different?
    def differenceTest(self, figArray1, figArray2, solArray):
        # Mask all values that are the same in each array
        result1 = np.copy(figArray1)
        result2 = np.copy(figArray2)
        result1[figArray1 == figArray2] = 255
        result2[figArray1 == figArray2] = 255
        result1 = Image.fromarray(result1, mode="L")
        result2 = Image.fromarray(result2, mode="L")

        result = chops.logical_and(result1.convert(mode="1"), result2.convert(mode="1"))

        result = result.convert(mode="L")
        result = np.array(result)

        # This is not really precise. The logical_and loses nested figures.
        # For example, a cross under a circle anded with a circle would lose the center of the cross.
        # Trying a looser percentile allowed for the match
        return self.isSameFigure(result, solArray, 4.0)


    def isDiagonalSameTest(self, aePixelRatio, solDiagRatios):
        if math.isclose(aePixelRatio['nw'], 0.0) and  math.isclose(aePixelRatio['ne'], 0.0) and math.isclose(aePixelRatio['sw'], 0.0) and math.isclose(aePixelRatio['se'], 0.0):
            for key, value in solDiagRatios.items():
                if math.isclose(value['nw'], 0.0) and  math.isclose(value['ne'], 0.0) and math.isclose(value['sw'], 0.0) and math.isclose(value['se'], 0.0):
                    self.vote(key, self.sameDiagonalVote)

    # Diagonal Top-Left to Bottom-Right Patterns
    # Same three images repeated in all figures. Diagonally, A=E=Solution. B=F=G, C=D=H
    # using Centered arrays
    # Trying ratios
    def topLeftPatternTest(self, a, b, c, d, e, f, g, h, solArray):
        if self.isSameFigure(b, f) and self.isSameFigure(f, g):
            if self.isSameFigure(c, d) and self.isSameFigure(d, h):
                if self.isSameFigure(a, e):
                    if self.isSameFigure(e, solArray):
                        return self.getSimilarity(a, solArray)
                    else:
                        return 100
                else:
                    return 100
            else:
                return 100
        else:
            return 100

    # Diagonal Top-Right to Bottom-Left Patterns
    # Same three images repeated in all figures. Diagonally, C=E=G. A=F=H, B=D=Solution
    def topRightPatternTest(self, a, b, c, d, e, f, g, h, solArray):
        if self.isSameFigure(c, e) and self.isSameFigure(e, g):
            if self.isSameFigure(a, f) and self.isSameFigure(f, h):
                if self.isSameFigure(b, d):
                    if self.isSameFigure(b, solArray):
                        return self.getSimilarity(d, solArray)
                    else:
                        return 100
                else:
                    return 100
            else:
                return 100
        else:
            return 100

    def topBottomSplitTest(self, topArray, bottomArray, solArray):
        figHalves1 = np.vsplit(topArray, 2)
        figHalves2 = np.vsplit(bottomArray, 2)

        newArray = np.concatenate((figHalves1[0], figHalves2[1]))

        return self.isSameFigure(newArray, solArray)

    # TESTS - All RPMs---------------------------------------------------------------------------------------------------------------------------------
    # Is image in figure flipped up or down? If so, its eastern and western quads will swap
    def isUpDownFlip(self, figArray, solArray):
        flipFig = np.flipud(figArray)

        result = np.bitwise_xor(solArray, flipFig)
        nonZero = np.count_nonzero(result)
        return nonZero < (.01 * result.size)

    # Is image in figure flipped left or right? If so, its northern and souther quadrants will swap
    def isLeftRightFlip(self, figArray, solArray):
        flipFig = np.fliplr(figArray)
        result = np.bitwise_xor(solArray, flipFig)
        nonZero = np.count_nonzero(result)
        return nonZero < (.010 * result.size)

    def isSameFigure(self, figArray, solArray, percent=None):
        if percent is None:
            percent = 1.5
        figImg = Image.fromarray(figArray, "L")
        solImg = Image.fromarray(solArray, "L")


        diffImg = chops.difference(figImg, solImg)

        difference = np.array(diffImg)
        # dark pixels (0) are the only differences
        no_change = np.count_nonzero(difference)

        return (no_change/difference.size) * 100 < percent

    def getSimilarity(self, figArray, solArray):
        figImg = Image.fromarray(figArray, "L")
        solImg = Image.fromarray(solArray, "L")
        diffImg = chops.difference(figImg, solImg)

        difference = np.array(diffImg)
        # dark pixels (0) are the only differences
        no_change = np.count_nonzero(difference)

        return no_change/difference.size * 100

    def centerImageArray(self, figArray):
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

    # VOTING---------------------------------------------------------------------------------------------------------------------------------

    def vote(self, solution, increment):
        self.votes[solution] += increment

    def getMostVotes(self):
        mostVoteList =  {}
        mostVotes = max(self.votes.values())
        gen = ((key,value) for (key,value) in self.votes.items() if value == mostVotes)
        mostVoteList = dict(gen)

        if len(mostVoteList) == 1:
            return int(max(mostVoteList, key=mostVoteList.get))
        else:
            return -1
