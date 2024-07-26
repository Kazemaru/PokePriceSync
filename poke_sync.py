from pokemontcgsdk import RestClient
import poke_func
import argparse

parser = argparse.ArgumentParser(prog='PokemonTCGPriceSync',description='Synchronize and fill entries for google sheets template',epilog='text help')

parser.add_argument('poke_api', type=str, help="Key for the PokemonTCG.io API")
parser.add_argument('google_api_file', type=str, help="Path for the JSON file containing the google API key")
parser.add_argument('spreadsheet_id', type=str, help="Google Sheet identifier (Obtainable by copying the id from the link)")
parser.add_argument('sheet_name', type=str, help="Name of the target sheet to update")
parser.add_argument('set_id', type=str, help="Code for the target set. Example format: 'swsh1' is the first set of the Sword and Shield gen")
args = parser.parse_args()


poke_api = args.poke_api
google_api_file = args.google_api_file
spreadsheet_id = args.spreadsheet_id
sheet_name = args.sheet_name
set_id = args.set_id

RestClient.configure(poke_api)

card_price_list = poke_func.getAllCardsPricesbySetId(set_id) #get the cards in the set
tg_set=poke_func.get_separate_TG_set(set_id) #get the trainer galery (if it exists)
if tg_set:
    tg_price_list = poke_func.getTGPricesbySetId(tg_set)
    card_price_list= card_price_list + tg_price_list

setsize = len(card_price_list)
cell_range="A2:D"+str(1+setsize)

poke_func.batch_update_values(spreadsheet_id, sheet_name+"!"+cell_range, 'USER_ENTERED', card_price_list, google_api_file)



