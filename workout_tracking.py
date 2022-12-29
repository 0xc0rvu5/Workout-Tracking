import requests, os
from datetime import datetime


#initiliaze global variables
GENDER = 'male'
WEIGHT = os.getenv('WEIGHT')
HEIGHT = os.getenv('HEIGHT')
AGE = int(os.getenv('AGE'))
KG = round(float(WEIGHT) / 2.2046)
CM = round(float(HEIGHT) * 2.54)
NUTRITIONIX_APP_ID = os.getenv('NUTRITIONIX_APP_ID')
NUTRITIONIX_API_KEY = os.getenv('NUTRITIONIX_API')
NUTRITIONIX_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'
SHEETY_SHEET_NAME = 'workout'
SHEETY_ENDPOINT = os.getenv('SHEETY_ENDPOINT')
TODAY = datetime.now().strftime('%d/%m/%Y')
CURRENT_TIME = datetime.now().strftime('%X')
#nutritionix relevant
HEADERS = {
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_API_KEY,
}


def add_exercise():
    '''Use pre-configured variables or fill in all relevant data needed to complete request.'''
    os.system('clear')
    choice = input(f'Gender: {GENDER}\nWeight: {WEIGHT}\nHeight: {HEIGHT}\nAge: {AGE}\nNutritionix App ID: {NUTRITIONIX_APP_ID}\nNutritionix API: {NUTRITIONIX_API_KEY}\nSheety sheet name: {SHEETY_SHEET_NAME}\nSheety endpoint: {SHEETY_ENDPOINT}\nAre all of these correct? "y"\n ~ ')
    if choice == 'y':
        exercise = input('What exercise did you complete?\n ~ ')
        parameters = {
            'query': exercise,
            'gender': GENDER,
            'weight_kg': KG,
            'height_cm': CM,
            'age': AGE,
        }
        #convert global variables to relevant local variables
        sheety_endpoint = SHEETY_ENDPOINT
        headers = HEADERS
        sheet = SHEETY_SHEET_NAME
    else:
        exercise = input('What exercise did you complete?\n ~ ')
        gender = input('Gender:\n ~ ')
        choice_2 = int(input('1: km and cm\n2. pounds and inches\n ~ '))
        if choice_2 == 1:
            kg = float(input('Weight:\n ~ '))
            cm = float(input('Height:\n ~ '))
        else:
            weight = float(input('Weight:\n ~ '))
            height = float(input('Height:\n ~ '))
            kg = round(float(weight) / 2.2046)
            cm = round(float(height) * 2.54)
        age = int(input('Age:\n ~ '))
        nutritionix_id = input('Nutritionix App ID:\n ~ ')
        nutritionix_api = input('Nutritionix API:\n ~ ')
        sheet = input('Sheety sheet name:\n ~ ')
        sheety_endpoint = input('Sheety endpoint:\n ~ ')
        parameters = {
            'query': exercise,
            'gender': gender,
            'weight_kg': kg,
            'height_cm': cm,
            'age': age,
        }
        headers = {
            'x-app-id': nutritionix_id,
            'x-app-key': nutritionix_api,
        }
    
    #fetch relevant nutritionix json formatted data
    response = requests.post(url=NUTRITIONIX_ENDPOINT, json=parameters, headers=headers)
    result = response.json()

    #iterate over nutritionix json output and place it into the corresponding sheety structure to upload to google spreadsheet then
    #print sheety response
    for exercise in result['exercises']:
        sheety_parameters = {
            f'{sheet}': {
                'date': TODAY,
                'time': CURRENT_TIME,
                'exercise': exercise['name'].title(),
                'duration': exercise['duration_min'],
                'calories': exercise['nf_calories'],
            }
        }

        sheety_response = requests.post(
            sheety_endpoint,
            json=sheety_parameters,
            auth=(
                os.environ['SHEETY_UNAME'],
                os.environ['SHEETY_PW'],
            )
        )

        print(sheety_response.text)


#execute function
try:
    add_exercise()

except KeyboardInterrupt:
    print('\nSee you later.')
