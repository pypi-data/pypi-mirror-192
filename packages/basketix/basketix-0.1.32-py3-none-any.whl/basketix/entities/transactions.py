'''Transactions entities module'''

class Transactions():
    GAME_CONFIG = 'GameConfig'

    DRAFT_PICK = 'DraftPick'

    FREE_AGENCY = 'FreeAgency'
    BID = f'{FREE_AGENCY}Bid'
    BID_DELETE = f'{FREE_AGENCY}BidDelete'
    CUT = f'{FREE_AGENCY}Cut'
