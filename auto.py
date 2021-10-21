from typing import List
from dataclasses import dataclass, field
import copy
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

PavementCache = []
LaneCache = []

class myValidator(Validator):

    def __init__(self, type_=None, min_=None, max_=None, range_=None) -> None:
        self.type_ = type_
        self.min_ = min_
        self.max_ = max_
        self.range_ = range_

    def validate(self, document):
        ui = document.text

        if self.type_ is not None:
            try:
                ui = self.type_(ui)
            except ValueError:
                raise ValidationError(message='This input contains non-numeric characters')
        if self.max_ is not None and ui > self.max_:
            raise ValidationError(message="Input must be less than or equal to {0}.".format(self.max_))
        elif self.min_ is not None and ui < self.min_:
            raise ValidationError(message="Input must be greater than or equal to {0}.".format(self.min_))
        elif self.range_ is not None and ui not in self.range_:
            if isinstance(self.range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                raise ValidationError(message=template.format(self.range_))
            else:
                template = "Input must be {0}."
                if len(self.range_) == 1:
                    raise ValidationError(message=template.format(*self.range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in self.range_[:-1]),
                        str(self.range_[-1])
                    ))
                    raise ValidationError(message=template.format(expected))

@dataclass
class StationInfo:
    isStationConvert: bool
    stationRef: float = 0.0
    stationOffRef: float = 0.0
    mileRef: float = 0.0
    
    def inputData(self):
        self.stationRef = float(prompt('Station Reference Point: ', validator=myValidator(float,0)))
        self.stationOffRef = float(prompt('Station Reference Offset Point: ', validator=myValidator(float,0)))
        self.mileRef = float(prompt('Mile Post Reference: ', validator=myValidator(float,0)))

@dataclass
class Segment:
    '''Object for tracking physical books in a collection.'''
    isMile: bool
    stInfo: StationInfo
    stationBegin: int = 0
    stationEnd: int = 0
    stationOffBegin: float = 0.0
    stationOffEnd: float = 0.0
    mileBegin: float = 0.0
    mileEnd: float = 0.0
    pavementType: str = ""
    
    def inputData(self):
        print('')
        if self.isMile == True:
            self.mileBegin = float(prompt('Mile Post Begin: ', validator=myValidator(float,0)))
            self.mileEnd = float(prompt('Mile Post End: ', validator=myValidator(float,0)))
        else:
            self.stationBegin = float(prompt('Station Begin: ', validator=myValidator(float,0)))
            self.stationOffBegin = float(prompt('Station Offset Begin: ', validator=myValidator(float,0)))
            self.stationEnd = float(prompt('Station End: ', validator=myValidator(float,0)))
            self.stationOffEnd = float(prompt('Station Offset End: ', validator=myValidator(float,0)))

        pavementCompleter = WordCompleter(PavementCache, sentence=True, ignore_case=True)
        self.pavementType = prompt('Pavement Type: ', completer=pavementCompleter, complete_while_typing=True)
        if self.pavementType not in PavementCache:
            PavementCache.append(self.pavementType)
        
    def processData(self):
        if self.isMile == False and self.stInfo.isStationConvert == True:
            self.mileBegin = ((100*self.stationBegin+self.stationOffBegin) - (100*self.stInfo.stationRef+self.stInfo.stationOffRef))/5280 + self.stInfo.mileRef
            self.mileEnd = ((100*self.stationEnd+self.stationOffEnd) - (100*self.stInfo.stationRef+self.stInfo.stationOffRef))/5280 + self.stInfo.mileRef
        
    def outputData(self):
        print("Output")

    def __str__(self):
        return str(self.mileBegin) + "," + str(self.mileEnd) + "," + str(self.pavementType)

@dataclass
class Lane:
    '''Object for tracking physical books in a collection.'''
    isMile: bool
    stInfo: StationInfo
    laneNumber: int = 0
    segments: list = field(default_factory=list,init=False)

    def __post_init__(self):
        self.segments = []

    def inputData(self):
        print('\nLane ' + str(self.laneNumber))

        anotherLane = 'y'
        while anotherLane == 'y' or anotherLane == '':
            tempSegment = Segment(self.isMile, self.stInfo)
            tempSegment.inputData()
            self.segments.append(tempSegment)
            anotherLane = str.lower(prompt("Do you have another segment [Y]? ", validator=myValidator(str.lower, range_=['y', 'n', ''])))

    def processData(self):
        for lSegment in self.segments:
            lSegment.processData()

    def outputData(self):
        print("Output")

    def __str__(self):
        myStr = ""
        for x in self.segments:
            myStr += str(x) + "; "

        return "Lane #" + str(self.laneNumber) + "- (Begin,End,Type) = " + myStr

@dataclass
class Highway:
    '''Object for tracking physical books in a collection.'''
    name: str = ""
    direction: str = ""
    lanes: list = field(default_factory=list,init=False)
    lanesSecondary: list = field(default_factory=list,init=False)
    laneCount: int = 0
    laneSecondaryCount: int = 0
    isBiDirection: bool = True
    isBiCopied: bool = True
    isMilePost: bool = False
    stInfo: StationInfo = None

    S_dirDict = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }

    def __post_init__(self):
        self.lanes = []
        self.lanesSecondary = []

    def inputData(self):
        global LaneCache
        self.name = prompt("Highway Name: ", validator=myValidator(str))
        self.direction = str.upper(prompt("Primary Direction: (N,S,E,W): ", validator=myValidator(str.upper, range_=['N', 'S', 'E', 'W'])))
        secDir = Highway.S_dirDict[self.direction]
        tempDirS = self.direction
        tempBi = str.lower(prompt("Lanes in Both Directions [Y]?: ", validator=myValidator(str.lower, range_=['y', 'n', ''])))
        if tempBi == 'n':
            self.isBiDirection = False

        if self.isBiDirection == True:
            tempBiCopy = str.lower(prompt("Is Secondary Direction Copied from First [Y]?: ", validator=myValidator(str.lower, range_=['y', 'n', ''])))
            if tempBiCopy == 'n':
                
                self.isBiCopied = False
            else:
                tempDirS = self.direction + " & " + secDir
        
        tempMile = str.lower(prompt("Are Segments in Miles or Stations (M = Miles, S = Stations)? ", validator=myValidator(str.lower, range_=['m', 's'])))
        if tempMile == 'm':
            self.isMilePost = True

        if self.isMilePost == False:
            tempStConv = str.lower(prompt("Would you like to convert Stations (Sta) and Mile Posts (MP) [Y]? ", validator=myValidator(str.lower, range_=['y', 'n', ''])))
            if tempStConv == "n":
                self.stInfo = StationInfo(False)
            else:
                self.stInfo = StationInfo(True)
                self.stInfo.inputData()

        self.__inputLanes(tempDirS,True)
        if self.isBiCopied == False:
            self.__inputLanes(secDir,False)

    def __inputLanes(self,direction,isPrimary):
        tempLaneCount = int(prompt("Number of Lanes in " + direction +  ": ", validator=myValidator(int, 1)))
        if isPrimary == True:
            self.laneCount = tempLaneCount
        else:
            self.laneSecondaryCount = tempLaneCount
        for i in range(tempLaneCount):
            if len(LaneCache) == 0:
                inputOld = 'n'
            else:
                inputOld = str.lower(prompt("Should we use existing lane [N]? ", validator=myValidator(str.lower, range_=['y', 'n', ''])))

            if inputOld == 'y':
                for j in range(len(LaneCache)):
                    print(f'{str(j+1): <{2}}' + ": " + str(LaneCache[j]))
                laneCopyNum = int(prompt("What lane should we use (input number)? ", validator=myValidator(int, 1, len(LaneCache)+1)))
                tempLane = copy.deepcopy(LaneCache[laneCopyNum-1])
            else:
                tempLane = Lane(self.isMilePost, self.stInfo, laneNumber=(i+1))
                tempLane.inputData()
                LaneCache.append(tempLane)
            if isPrimary == True:
                self.lanes.append(tempLane)
            else:
                self.lanesSecondary.append(tempLane)    
            

    # TODO: Method to do any data processing. IE looking up location on map, finding distances, doing any math...
    # Highway.processData which calls many Lane.processData which calls many Segment.processData. That way we keep small functions that have single "functions". Do the same with outputData.
    def processData(self):
        for lLane in self.lanes:
            iLane.processData()

    # TODO: Method to flatten and output data to excel or another format. 
    # EXAMPLE:
    # This method takes the following one line and hierarchical data and flattens it into many rows. 
    # Highway(name='I10', direction='S', lanes=[Lane(laneNumber=1, pavementType='AB', segment=None), Lane(laneNumber=2, pavementType='PS', segment=None), Lane(laneNumber=3, pavementType='HI', segment=None)])
    # 
    # Output:
    # Highway, Direction, LaneNumber, Pavement Type, Segment Start, Segment End, Segment End
    # I10    , S        , 1         , AB           , None         , None       , None      
    # I10    , S        , 2         , PS           , None         , None       , None      
    # I10    , S        , 2         , HI           , None         , None       , None      

    def outputData(self):
        print("Output")

# Main code
highwayIC = Highway()
highwayIC.inputData()



print(highwayIC)
