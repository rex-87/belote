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
TapisRange = Range(0, 4)
EquipeRange = Range(0, 2)

PlayerDict = {
    0:'J1',
    1:'J2',
    2:'J3',
    3:'J4',
}

TapisDict = {
    0:'TAPIS0',
    1:'TAPIS1',
    2:'TAPIS2',
    3:'TAPIS3',
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
        'TAPIS0',
        'TAPIS1',
        'TAPIS2',
        'TAPIS3',
        'SCORE1',
        'SCORE2',
    ]

    SuitDict = {
        0:'Pique  ',
        1:'Coeur  ',
        2:'Carreau',
        3:'Trefle ',
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

    NumberToValue = {
        '7' : { 'NORMAL': 0, 'ATOUT': 0 },
        '8' : { 'NORMAL': 1, 'ATOUT': 1 },
        '9' : { 'NORMAL': 2, 'ATOUT': 6 },
        '10': { 'NORMAL': 6, 'ATOUT': 4 },
        'V' : { 'NORMAL': 3, 'ATOUT': 7 },
        'D' : { 'NORMAL': 4, 'ATOUT': 2 },
        'R' : { 'NORMAL': 5, 'ATOUT': 3 },
        'A' : { 'NORMAL': 7, 'ATOUT': 5 },
    }

    NumberToPoints = {
        '7' : { 'NORMAL': 0, 'ATOUT': 0 },
        '8' : { 'NORMAL': 0, 'ATOUT': 0 },
        '9' : { 'NORMAL': 0, 'ATOUT':14 },
        '10': { 'NORMAL':10, 'ATOUT':10 },
        'V' : { 'NORMAL': 2, 'ATOUT':20 },
        'D' : { 'NORMAL': 3, 'ATOUT': 3 },
        'R' : { 'NORMAL': 4, 'ATOUT': 4 },
        'A' : { 'NORMAL':11, 'ATOUT':11 },
    }
    
    def __init__(self, Number = None, Suit = None, State = 'UNDEALT'):
        self.Number = None
        self.Suit = None
        self.State = None
        self.Value = None

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

    def GetValue(self, bAtout = False):
        NumberString = self.NumberDict[self.GetNumber()]
        
        if bAtout:
            return self.NumberToValue[NumberString]['ATOUT']
        else:
            return self.NumberToValue[NumberString]['NORMAL']

    def GetPoints(self, bAtout = False):
        NumberString = self.NumberDict[self.GetNumber()]
        
        if bAtout:
            return self.NumberToPoints[NumberString]['ATOUT']
        else:
            return self.NumberToPoints[NumberString]['NORMAL']
            
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
                
        self.TapisList = []
        self.Atout = None
        self.DealingPlayer = None
        self.FirstPlayer = None
        self.DixDeDer = None
        
    def Shuffle(self):
        for i in range(1000):
            RandInt = random.randrange(1, SuitRange.Max*NumberRange.Max)
            temp = self[0]
            self[0] = self[RandInt]
            self[RandInt] = temp
            
    def Deal(self, DealingPlayer = None):
        if DealingPlayer is None:
            raise BeloteException('DealingPlayer parameter cannot be None')
        
        self.DealingPlayer = DealingPlayer
        self.FirstPlayer = (self.DealingPlayer + 1)%TapisRange.Max
        
        i = 0
        
        while i < PlayerRange.Max*3:
            for j_ in range(PlayerRange.Max):
                j = (DealingPlayer + j_ + 1)%PlayerRange.Max
                for u in range(3):
                    self[i+u].SetState(PlayerDict[j])
                else:
                    i += 3

        while i < PlayerRange.Max*3 + PlayerRange.Max*2:            
            for j_ in range(PlayerRange.Max):
                j = (DealingPlayer + j_ + 1)%PlayerRange.Max        
                for u in range(2):              
                    self[i+u].SetState(PlayerDict[j])
                else:
                    i += 2                    
        
        RandInt = random.randrange(0, PlayerRange.Max)
        self[PlayerRange.Max*3+PlayerRange.Max*2].SetState(PlayerDict[RandInt])
        self.Atout = self[PlayerRange.Max*3+PlayerRange.Max*2].GetSuit()
        
        i = PlayerRange.Max*3+PlayerRange.Max*2+1
        while i < SuitRange.Max*NumberRange.Max:
            for j_ in range(PlayerRange.Max):
                j = (DealingPlayer + j_ + 1)%PlayerRange.Max            
                for u in range(3):             
                    if j != RandInt or u != 2:                     
                        self[i+u].SetState(PlayerDict[j])
                    else:
                        i += 2
                        break
                else:
                    i += 3
    
    def GetPlayerPack(self, Player = None):
        if Player is None:
            raise BeloteException('Player parameter cannot be None')
        
        PlayerPack = Pack()
        for CardObject in self:
            if CardObject.GetState() == PlayerDict[Player]:
                PlayerPack.append(CardObject)
        return PlayerPack

    def GetTapisPack(self):
        
        TapisPack = Pack()
        
        for CardObject in self:
            if CardObject.GetState() == 'TAPIS0':
                TapisPack.append(CardObject)   

        for CardObject in self:
            if CardObject.GetState() == 'TAPIS1':
                TapisPack.append(CardObject)               
                
        for CardObject in self:
            if CardObject.GetState() == 'TAPIS2':
                TapisPack.append(CardObject)             
                
        for CardObject in self:
            if CardObject.GetState() == 'TAPIS3':
                TapisPack.append(CardObject)             

        return TapisPack

    def ToTapisPack(self, Player = None, PlayerPackIndex = None):        

        TapisListSize = len(self.TapisList)
        
        PlayerPack = self.GetPlayerPack(Player)
        
        # check state is Jx
        CurrentState = PlayerPack[PlayerPackIndex].GetState()
        for j in range(PlayerRange.Max):
            if CurrentState == PlayerDict[j]:
                break
        else:
            raise BeloteException('State {!r} is unexpected'.format(CurrentState))
        
        PlayerPack[PlayerPackIndex].SetState('TAPIS{}'.format(TapisListSize))
        self.TapisList.append(None)        

    def CheckPlayerMove(self, Player = None, PlayerPackIndex = None):
        
        PlayerPack = self.GetPlayerPack(Player)
        
        CardToPlay = PlayerPack[PlayerPackIndex]
        
        TapisPack = self.GetTapisPack()
        
        # check playing move is allowed
        if TapisPack != []:
            CouleurDemandee = TapisPack[0].GetSuit()

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

        TapisPack = self.GetTapisPack()    
        
        for i in range(len(TapisPack)):
            # check state is TAPISx
            CurrentState = TapisPack[i].GetState()
            for e in range(TapisRange.Max):         
                if CurrentState == TapisDict[e]:
                    break
            else:
                raise BeloteException('State {!r} is unexpected'.format(CurrentState))
            
            TapisPack[i].SetState(EquipeDict[Equipe])
            
        self.TapisList = []

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
  
    def GetWinningTapisPackIndex(self):
        TapisPack = self.GetTapisPack() 
        
        WinningTapisPackIndex = 0
        FirstCardSuit = TapisPack[0].GetSuit()
        MaxValue = TapisPack[0].GetValue(FirstCardSuit == self.Atout)    
        bAtoutJoue = (FirstCardSuit == self.Atout)
        for TapisPackIndex_, card in enumerate(TapisPack[1:]):
            
            TapisPackIndex = TapisPackIndex_ + 1
            
            CardSuit = card.GetSuit()
            if bAtoutJoue:
                if CardSuit != self.Atout:
                    continue
                else:
                    CardValue = card.GetValue(bAtout = True)
                    if CardValue > MaxValue:
                        MaxValue = CardValue
                        WinningTapisPackIndex = TapisPackIndex                   
            else:
                if CardSuit == self.Atout:
                    bAtoutJoue = True
                    CardValue = card.GetValue(bAtout = True)
                    MaxValue = CardValue
                    WinningTapisPackIndex = TapisPackIndex
                else:
                    if CardSuit != FirstCardSuit:
                        continue
                    else:
                        CardValue = card.GetValue(bAtout = False)
                        if CardValue > MaxValue:
                            MaxValue = CardValue
                            WinningTapisPackIndex = TapisPackIndex
        
        return WinningTapisPackIndex
    
    def Player2Equipe(self, Player = None):
        if Player is None:
            raise BeloteException('Player parameter cannot be None')

        if Player == 0 or Player == 2:
            return 0
        elif Player == 1 or Player == 3:
            return 1
        else:
            raise BeloteException('Player parameter must be 0-3. Player = {!r}'.format(Player))
    
    def GetScore(self, Equipe = None):
        ScorePack = self.GetScorePack(Equipe)
        
        Score = 0
        for card in ScorePack:
            CardSuit = card.GetSuit()
            CardValue = card.GetPoints(CardSuit == self.Atout)
            Score += CardValue
            
        # Dix de der
        if self.DixDeDer == Equipe:
            Score += 10
            
        return Score

class Belote(object):
    def __init__(self):        
        
        BelotePackObject = BelotePack()

        BelotePackObject.Shuffle()

        BelotePackObject.Deal(DealingPlayer = 3)

        # print BelotePackObject
        
        print 'Atout:', Card.SuitDict[BelotePackObject.Atout]

        for t in range(8): # that many rounds
        
            print 'Tour {} ----------------------------'.format(t+1)
            
            for j_ in range(TapisRange.Max): # for each player. TODO: index qui depend du DealingPlayer
                
                j = (BelotePackObject.FirstPlayer + j_)%PlayerRange.Max
                
                print PlayerDict[j]
                
                PlayerPack = BelotePackObject.GetPlayerPack(j)
                print PlayerPack
                for PlayerPackIndex, card in enumerate(PlayerPack): 
                    if BelotePackObject.CheckPlayerMove(j, PlayerPackIndex): # premiere carte qui est valide
                        BelotePackObject.ToTapisPack(j, PlayerPackIndex) # joue la
                        break
                print "Tapis:"                        
                print BelotePackObject.GetTapisPack()
            
            WinningTapisPackIndex = BelotePackObject.GetWinningTapisPackIndex()
            print 'WinningPlayer:', WinningTapisPackIndex
            
            WinningPlayer = (BelotePackObject.FirstPlayer + WinningTapisPackIndex)%PlayerRange.Max
            BelotePackObject.ToScorePack(BelotePackObject.Player2Equipe(WinningPlayer)) # mets les cartes jouees dans la pile des scores
            
            # Dix de der
            if t == 7:
                BelotePackObject.DixDeDer = BelotePackObject.Player2Equipe(WinningPlayer)
            
            print "ScorePack1:"
            print BelotePackObject.GetScorePack(0)
            print "Score1:", BelotePackObject.GetScore(0)
            print "ScorePack2:"            
            print BelotePackObject.GetScorePack(1)
            print "Score2:", BelotePackObject.GetScore(1)
            
            BelotePackObject.FirstPlayer = WinningPlayer
            
        # print BelotePackObject
        
BeloteObject = Belote()