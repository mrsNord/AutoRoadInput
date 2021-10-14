from typing import List
from dataclasses import dataclass, field
import copy

SegmentCache = []
LaneCache = []


def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return ui

@dataclass
class Segment:
    '''Object for tracking physical books in a collection.'''
    segmentBegin: float = 0.0
    segmentEnd: float = 0.0
    isMilePost: bool = False
    pavementType: str = ""

    def inputData(self):
        print('')
        self.segmentBegin = sanitised_input("Segment Begin: ", int) 
        self.segmentEnd = sanitised_input("Segment End: ", int)
        tempMile = sanitised_input("Is this a mile post (Y,N)? ", str.lower, range_=['y', 'n'])
        if tempMile == 'y':
            self.isMilePost = True

        self.pavementType = sanitised_input("Pavement Type (enter to end)? ", str)

        
    def processData(self):
        print("Process")
        
    def outputData(self):
        print("Output")

    def __str__(self):
        return str(self.segmentBegin) + "," + str(self.segmentEnd) + "," + str(self.isMilePost) + "," + str(self.pavementType)

@dataclass
class Lane:
    '''Object for tracking physical books in a collection.'''
    laneNumber: int = 0
    segments: list = field(default_factory=list,init=False)

    def __post_init__(self):
        self.segments = []

    def inputData(self):
        print('\nLane ' + str(self.laneNumber))

        anotherLane = 'y'
        while anotherLane == 'y' or anotherLane == '':
            if len(SegmentCache) == 0:
                inputOld = 'n'
            else:
                inputOld = sanitised_input("Should we use existing segment [N]? ", str.lower, range_=['y', 'n', ''])

            if inputOld == 'y':
                print("Segments: Format (Begin,End,isMile,Type)")
                for i in range(len(SegmentCache)):
                    print(f'{str(i+1): <{2}}' + "  : " + str(SegmentCache[i]))
                segmentCopyNum = sanitised_input("What segment should we use (input number)? ", int, 1, len(SegmentCache)+1)
                tempSegment = copy.deepcopy(SegmentCache[segmentCopyNum-1])
            else:
                tempSegment = Segment()
                tempSegment.inputData()
                SegmentCache.append(tempSegment)
            self.segments.append(tempSegment)
            anotherLane = sanitised_input("Do you have another segment [Y]? ", str.lower, range_=['y', 'n', ''])

    def processData(self):
        print("Process")

    def outputData(self):
        print("Output")

    def __str__(self):
        myStr = ""
        for x in self.segments:
            myStr += str(x) + "; "

        return "Lane #" + str(self.laneNumber) + "- (Begin,End,isMile,Type) = " + myStr

@dataclass
class Highway:
    '''Object for tracking physical books in a collection.'''
    name: str = ""
    direction: str = ""
    lanes: list = field(default_factory=list,init=False)
    laneCount = 0

    def __post_init__(self):
        self.lanes = []

    def inputData(self):
        global LaneCache
        self.name = sanitised_input("Highway Name: ", str)
        self.direction = sanitised_input("Direction: (N,S,E,W): ", str.upper, range_=['N', 'S', 'E', 'W'])
        self.laneCount = sanitised_input("Number of Lanes: ", int, 1)  
        for i in range(self.laneCount):
            if len(LaneCache) == 0:
                inputOld = 'n'
            else:
                inputOld = sanitised_input("Should we use existing lane [N]? ", str.lower, range_=['y', 'n', ''])

            if inputOld == 'y':
                for j in range(len(LaneCache)):
                    print(f'{str(j+1): <{2}}' + ": " + str(LaneCache[j]))
                laneCopyNum = sanitised_input("What lane should we use (input number)? ", int, 1, len(LaneCache)+1)
                tempLane = copy.deepcopy(LaneCache[laneCopyNum-1])
            else:
                tempLane = Lane(laneNumber=(i+1))
                tempLane.inputData()
                LaneCache.append(tempLane)
            self.lanes.append(tempLane)

    # TODO: Method to do any data processing. IE looking up location on map, finding distances, doing any math...
    # Highway.processData which calls many Lane.processData which calls many Segment.processData. That way we keep small functions that have single "functions". Do the same with outputData.
    def processData(self):
        print("Process")

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
