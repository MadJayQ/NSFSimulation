#TraCI POI Module
#Origin: /sumo_master/modules/poi.py
#Created By : Aleck Johnson
#   Also By : Quentin Goss
#Last Modified By : Quentin Goss
#Date Last Modified: 07/26/2018
#Status: Functional and Tested
class poi:        
    def __init__(self, ps_ID, pf_CoordX, pf_CoordY, pf_Value, ps_sff_ClosestEdge):
        self.s_ID = ps_ID
        self.f_CoordX = pf_CoordX
        self.f_CoordY = pf_CoordY
        self.f_CoordZ = 0.0
        self.f_Value = pf_Value
        self.f_DecreaseValue = 1.0
        self.f_IncreaseValue = 1.0
        self.s_LastVehID = ""
        self.n_LastHitTime = -1
        self.n_NumHits = 0
        self.s_sff_ClosestEdge = ps_sff_ClosestEdge
    
    def __del__(self): #default deconstructor
        del self.s_ID
        del self.f_CoordX
        del self.f_CoordY
        del self.f_CoordZ
        del self.f_Value
        del self.s_LastVehID
        del self.n_LastHitTime
        del self.n_NumHits
        del self.s_sff_ClosestEdge
        

        
#Setters/Getters Begin Below
    def getID(self):
        return self.s_ID
    def setID(self,s_newID):
        self.s_ID = s_newID

    def getXCoord(self):
        return self.f_CoordX
    def setXCoord(self,f_newX):
        self.f_CoordX = f_newX

    def getYCoord(self):
        return self.f_CoordY
    def setYCoord(self,f_newY):
        self.f_CoordY = f_newY

    def getZCoord(self):
        return self.f_CoordZ
    def setZCoord(self,f_newZ):
        self.f_CoordZ = f_newZ

    def getValue(self):
        return self.f_Value
    def setValue(self,f_newVal):
        self.f_Value = f_newVal
        
    def getIncreaseValue(self):
        return self.f_IncreaseValue
    def setIncreaseValue(self,pf_IncreaseValue):
        self.f_IncreaseValue = pf_IncreaseValue
        
    def getDecreaseValue(self):
        return self.f_DecreaseValue
    def setDecreaseValue(self,pf_DecreaseValue):
        self.f_DecreaseValue = pf_DecreaseValue

    def getLastVehID(self):
        return self.s_LastVehID
    def setLastVehID(self,n_newVehID):
        self.s_LastVehID = n_newVehID

    def getLastHitTime(self):
        return self.n_LastHitTime
    def setLastHitTime(self,n_newHitTime):
        self.n_LastHitTime = n_newHitTime

    def getHitTotal(self):
        return self.n_NumHits
    def setHitTotal(self,n_newHitTotal):
        self.n_NumHits = n_newHitTotal
        
    def getClosestEdge(self):
        return self.s_sff_ClosestEdge
    def setClosestEdge(self,s_sff_Edge):
        self.s_sff_ClosestEdge = s_sff_Edge
#End of Setters/Getters

    def increaseValue(self):
        self.f_Value += self.f_IncreaseValue
    def increaseValueBy(self,f_Amt):
        self.f_Value += f_Amt
    def decreaseValue(self):
        self.f_Value -= self.f_DecreaseValue
        if (self.f_Value < 0.0):
          self.f_Value = 0.0

    #############################
    # A vehicle tags the POI
    #
    # @param n_Step = current timestep
    # @param s_VehID = ID of the vehicle that hits the POI
    #############################
    def vehicleHit(self,n_step,s_vehID):
        #Obtain Vehicle ID
        self.s_LastVehID = s_vehID
        
        #get Current time and set to time of hit
        self.n_LastHitTime = n_step

        # The value decreases
        self.decreaseValue()
        
        self.n_NumHits += 1
    # end def vehicleHit(n_Step,s_VehID):
