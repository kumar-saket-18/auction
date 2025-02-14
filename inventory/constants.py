import enum


class AppConstants:
    # Constants
    MIN_PRICE = 20000

class ErrorStrings:
    INVALID_PRICE = 'Invalid price'
    TEAM_FULL = 'Team is already full'
    INSUFFICIENT_BUDGET = 'Not enough budget to complete the team'
    INVALID_PLAYER = 'Player does not exist'
    INVALID_TEAM = 'Team does not exist'
    MISSING_PLAYER_ID = 'Player ID is required'
    INVALID_PRICE_FORMAT = 'Price must be a valid number.'
    GENERIC_ERROR = 'An unexpected error occurred. Please try again.'
    MISSING_PARAMETERS = 'Required parameters are missing.'

class SuccessMessages:
    PLAYER_ADDED = "%s will play for  %s in Mahabharata 3.0"
    PLAYER_MARKED_AS_UNSOLD = "%s remain unsold"

class AuctionLogsActionEnum(enum.Enum):
    SOLD = "sold"
    UNSOLD = "unsold"