import random

class BeloteException(Exception):
    pass

class Range(object):
    def __init__(self, RangeMin = None, RangeMax = None):
        self.Min = RangeMin
        self.Max = RangeMax
    
NumberRange = Range(0, 8) 
SuitRange = Range(0, 4)
PlayerRange = Range(0, 4)
PlayedRange = Range(0, 4)
EquipeRange = Range(0, 2)

PlayerDict = {
    0:'J1',
    1:'J2',
    2:'J3',
    3:'J4',
}

PlayedDict = {
    0:'PLAYED0',
    1:'PLAYED1',
    2:'PLAYED2',
    3:'PLAYED3',
}

EquipeDict = {
    0:'SCORE1',
    1:'SCORE2',
}    
    
def _CheckParameterType(Parameter = None, Type = None, ParameterName = None):
    if not isinstance(Parameter, int):
        raise BeloteException('{} parameter is expected to be of type int. {} = {}, type({}) = {}'.format(ParameterName, ParameterName, Parameter, ParameterName, type(Parameter)))    
    
class Card(object):
    StateList = [
        'UNDEALT',
        'J1',
        'J2',
        'J3',
        'J4',
        'PLAYED0',
        'PLAYED1',
        'PLAYED2',
        'PLAYED3',
        'SCORE1',
        'SCORE2',
    ]

    SuitDict = {
        0:'Pique',
        1:'Coeur',
        2:'Carrx',
        3:'Trefl',
    }
    
    NumberDict = {
        0:'7',
        1:'8',
        2:'9',
        3:'10',
        4:'V',
        5:'D',
        6:'R',
        7:'A',
    }
        
    def __init__(self, Number = None, Suit = None, State = 'UNDEALT'):
        self.Number = None
        self.Suit = None
        self.State = None

        self.SetNumber(Number)
        self.SetSuit(Suit)
        self.SetState(State)
    
    def __repr__(self):
        return "Card(Suit = {!r}, Number = {!r}, State = {!r})".format(self.GetSuit(), self.GetNumber(), self.GetState())

    def __str__(self):
        return '{}-{:>2} {!r}'.format(self.SuitDict[self.Suit], self.NumberDict[self.Number], self.State)
        
    def GetNumber(self):
        return self.Number
        
    def SetNumber(self, Number):
        _CheckParameterType(Number, int, 'Number')
        if Number < NumberRange.Min or Number >= NumberRange.Max:
            raise BeloteException('Valid values for Number parameter: 0-7. Number = {}'.format(Number))        
        self.Number = Number

    def GetSuit(self):
        return self.Suit
        
    def SetSuit(self, Suit):
        _CheckParameterType(Suit, int, 'Suit')
        if Suit < SuitRange.Min or Suit >= SuitRange.Max:
            raise BeloteException('Valid values for Suit parameter: 0-4. Suit = {}'.format(Suit))        
        self.Suit = Suit

    def GetState(self):
        return self.State
        
    def SetState(self, State):
        if State not in self.StateList:
            raise BeloteException('State {!r} is not a valid state. Valid States = {}'.format(State, self.StateList))
        self.State = State

class Pack(list):
    def __init__(self):
        list.__init__(self)

    def __repr__(self):
        ReprOut = ''
        for i, Card in enumerate(self):
            ReprOut += '{!r}: {!r}\n'.format(i, Card)
        return ReprOut

    def __str__(self):
        if self == []:
            return 'EMPTY' 
        ReprOut = ''
        for i, Card in enumerate(self):
            ReprOut += '{!r:>02}: {!s}\n'.format(i, Card)
        return ReprOut
        
class BelotePack(Pack):
    def __init__(self):
        Pack.__init__(self)

        for Suit in range(SuitRange.Max):
            for Number in range(NumberRange.Max):
                CardObject = Card(Number = Number, Suit = Suit)
                self.append(CardObject)
                
        self.PlayedList = []
        self.Atout = None
        
    def Shuffle(self):
        for i in range(1000):
            RandInt = random.randrange(1, SuitRange.Max*NumberRange.Max)
            temp = self[0]
            self[0] = self[RandInt]
            self[RandInt] = temp
            
    def Deal(self):
        for j in range(PlayerRange.Max):
            for i in range(3):
                self[j*3+i].SetState(PlayerDict[j])

        for j in range(PlayerRange.Max):
            for i in range(2):
                self[PlayerRange.Max*3+j*2+i].SetState(PlayerDict[j])
        
        RandInt = random.randrange(0, PlayerRange.Max)
        self[PlayerRange.Max*3+PlayerRange.Max*2].SetState(PlayerDict[RandInt])
        self.Atout = self[PlayerRange.Max*3+PlayerRange.Max*2].GetSuit()
        
        i = PlayerRange.Max*3+PlayerRange.Max*2+1
        while i < SuitRange.Max*NumberRange.Max:
            for j in range(PlayerRange.Max):
                for u in range(3):             
                    if j != RandInt or u != 2:                     
                        self[i+u].SetState(PlayerDict[j])
                    else:
                        i += 2
                        break
                else:
                    i += 3
    
    def GetPlayerPack(self, Player = None):
        PlayerPack = Pack()
        for CardObject in self:
            if CardObject.GetState() == PlayerDict[Player]:
                PlayerPack.append(CardObject)
        return PlayerPack

    def GetPlayedPack(self):
        
        PlayedPack = Pack()
        
        for CardObject in self:
            if CardObject.GetState() == 'PLAYED0':
                PlayedPack.append(CardObject)   

        for CardObject in self:
            if CardObject.GetState() == 'PLAYED1':
                PlayedPack.append(CardObject)               
                
        for CardObject in self:
            if CardObject.GetState() == 'PLAYED2':
                PlayedPack.append(CardObject)             
                
        for CardObject in self:
            if CardObject.GetState() == 'PLAYED3':
                PlayedPack.append(CardObject)             

        return PlayedPack

    def ToPlayedPack(self, Player = None, PlayerPackIndex = None):        

        PlayedListSize = len(self.PlayedList)
        
        PlayerPack = self.GetPlayerPack(Player)
        
        # check state is Jx
        CurrentState = PlayerPack[PlayerPackIndex].GetState()
        for j in range(PlayerRange.Max):
            if CurrentState == PlayerDict[j]:
                break
        else:
            raise BeloteException('State {!r} is unexpected'.format(CurrentState))
        
        PlayerPack[PlayerPackIndex].SetState('PLAYED{}'.format(PlayedListSize))
        self.PlayedList.append(None)        

    def CheckPlayerMove(self, Player = None, PlayerPackIndex = None):
        
        PlayerPack = self.GetPlayerPack(Player)
        
        CardToPlay = PlayerPack[PlayerPackIndex]
        
        PlayedPack = self.GetPlayedPack()
        
        # check playing move is allowed
        if PlayedPack != []:
            for card in PlayedPack:
                if card.GetSuit() == self.Atout:
                    CouleurDemandee = self.Atout
                    break
            else:
                CouleurDemandee = PlayedPack[0].GetSuit()

            if CardToPlay.GetSuit() == CouleurDemandee:
                # print "C'est la couleur demandee!",
                return True
            else:            
                HasCouleurDemandee = self.HasCouleurDemandee(Player, CouleurDemandee)
                if HasCouleurDemandee:
                    # print 'Il faut jouer la couleur demandee!',              
                    return False
                else:
                    if CardToPlay.GetSuit() == self.Atout:
                        # print "C'est de l'atout!",
                        return True
                    else:                    
                        HasAtout = self.HasAtout(Player)
                        if HasAtout:
                            # print "Il faut jouer atout!",                 
                            return False
                        else:
                            # print "Il faut se defausser!",                  
                            return True

        else:
            return True       
            
    def GetScorePack(self, Equipe = None):
        
        ScorePack = Pack()
        
        for CardObject in self:
            if CardObject.GetState() == EquipeDict[Equipe]:
                ScorePack.append(CardObject)              

        return ScorePack

    def ToScorePack(self, Equipe = None):        

        PlayedPack = self.GetPlayedPack()    
        
        for i in range(len(PlayedPack)):
            # check state is PLAYEDx
            CurrentState = PlayedPack[i].GetState()
            for e in range(PlayedRange.Max):         
                if CurrentState == PlayedDict[e]:
                    break
            else:
                raise BeloteException('State {!r} is unexpected'.format(CurrentState))
            
            PlayedPack[i].SetState(EquipeDict[Equipe])
            
        self.PlayedList = []

    def HasCouleurDemandee(self, Player = None, CouleurDemandee = None):
        PlayerPack = self.GetPlayerPack(Player)
        
        for card in PlayerPack:
            if card.GetSuit() == CouleurDemandee:
                return True
        else:
            return False

    def HasAtout(self, Player = None):
        PlayerPack = self.GetPlayerPack(Player)
        
        for card in PlayerPack:
            if card.GetSuit() == self.Atout:
                return True
        else:
            return False
            
class Belote(object):
    def __init__(self):        
        
        BelotePackObject = BelotePack()

        BelotePackObject.Shuffle()

        BelotePackObject.Deal(DealingPlayer = None)

        print BelotePackObject
        
        print 'Atout:', Card.SuitDict[BelotePackObject.Atout]

        for t in range(8): # that many rounds
        
            print 'Tour {} ----------------------------'.format(t+1)
            
            for j in range(PlayedRange.Max): # for each player. TODO: index qui depend du DealingPlayer
                
                print PlayerDict[j]
                
                PlayerPack = BelotePackObject.GetPlayerPack(j)
                for PlayerPackIndex, card in enumerate(PlayerPack): 
                    if BelotePackObject.CheckPlayerMove(j, PlayerPackIndex): # premiere carte qui est valide
                        BelotePackObject.ToPlayedPack(j, PlayerPackIndex) # joue la
                        break
                print BelotePackObject.GetPlayedPack()      
            
            BelotePackObject.ToScorePack(0) # mets les cartes jouees dans la pile des scores
        
        # print BelotePackObject
        
BeloteObject = Belote()