from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import csv
import poke_set
from pokemontcgsdk import *


def getAllCardsPricesbySetId(setid):

    cardlist = Card.where(q='set.id:'+setid) #get all cards of the given set id
    cardsvalues = []
    for cardnum in range(0, len(cardlist)): #If extraction order matches the order
        print(str(cardnum+1))
        values = []
        if int(cardlist[cardnum].number) == int(cardnum+1):
            card = cardlist[cardnum]
            values.append(card.number)
            values.append(str(card.name))
            values.append(str(card.rarity))
            values.append(float(card.cardmarket.prices.avg7))
        elif int(cardlist[cardnum].number) != int(cardnum+1): #if the order does not match we need to obtain the correct card
            print("Searching for card")
            for card in cardlist:
                if int(card.number) == int(cardnum+1):
                    values.append(card.number)
                    values.append(str(card.name))
                    values.append(str(card.rarity))
                    values.append(float(card.cardmarket.prices.avg7))
                    print(values)
        cardsvalues.append(values)
    return cardsvalues

def getTGPricesbySetId(setid):
    cardlist = Card.where(q='set.id:'+setid) #get all cards of the given set id
    cardsvalues = []
    for card in cardlist:
        values=[]
        values.append(card.number)
        values.append(str(card.name))
        values.append(str(card.rarity))
        values.append(float(card.cardmarket.prices.avg7))
        cardsvalues.append(values)
    return cardsvalues


def update_values(spreadsheet_id, range_name, value_input_option, _values, google_api_file):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = ServiceAccountCredentials.from_json_keyfile_name(google_api_file)

  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    values=[]
    for v in _values:
       values.append([v])
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
  
def batch_update_values(spreadsheet_id, range_name, value_input_option, _values, google_api_file):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = ServiceAccountCredentials.from_json_keyfile_name(google_api_file)
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)

    values = [
        [
            # Cell values ...
        ],
        # Additional rows
    ]
    data = [
        {"range": range_name, "values": _values},
        # Additional ranges to update ...
    ]
    body = {"valueInputOption": value_input_option, "data": data}
    result = (
        service.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    print(f"{(result.get('totalUpdatedCells'))} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
  
def dump_rarities_to_csv():
    rarities=Rarity.all()
    with open('rarities.csv','w',newline='') as file:
        writer = csv.writer(file)
        for rarity in rarities:
            writer.writerow([rarity])

def get_separate_TG_set(set_id):
    if set_id in poke_set.sets_with_tg:
      tg_set = set_id+"tg"
      return tg_set
    else:
        return False