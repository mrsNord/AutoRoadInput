from typing import List

from dataclasses import dataclass
@dataclass
class Segment:
    '''Object for tracking physical books in a collection.'''
    segmentBegin: float = 0.0
    segmentEnd: float = 0.0
    isMilePost: bool = False
    pavementType: List[str] = None

    def inputData(self):
        print("Hi Segment")

@dataclass
class Lane:
    '''Object for tracking physical books in a collection.'''
    laneNumber: int = 0
    # pavementType[]: str

    segment: List[Segment] = None

    def inputData(self):
        print("Hi Lane " + str(self.laneNumber))

@dataclass
class Highway:
    '''Object for tracking physical books in a collection.'''
    name: str = ""
    direction: str = ""
    lanes: List[Lane] = None
    laneCount = 0

    def inputData(self):
        self.name = input("Highway Name: ")
        self.direction = input("Direction: (i.e. N, S)")
        self.laneCount = int(input("Number of Lanes: "))  
        self.lanes = []
        for i in range(self.laneCount):
            tempLane = Lane(laneNumber=(i+1))
            tempLane.inputData()
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
