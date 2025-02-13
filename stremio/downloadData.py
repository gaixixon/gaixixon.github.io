import requests
import json

def downloadData():
    # Specify the URL
    url = 'https://script.google.com/macros/s/AKfycbw8HZ8DgynbY8KW2e0pGMHRWwzs0nphV_ZFZwUoL_I2njlSNoal7YXfDk-wZkYCANKz/exec'
    try:
        response = requests.get(url + '?action=getcatalog')
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the JSON content
        data = response.json()
        # Save the JSON data to a file
        with open('catalog.json', 'w') as file:
            json.dump(data, file, indent=4)
            print('JSON data has been saved to catalog.json')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')



    try:
        response = requests.get(url + '?action=getmeta')
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the JSON content
        data = response.json()
        # Save the JSON data to a file
        with open('meta.json', 'w') as file:
            json.dump(data, file, indent=4)
            print('JSON data has been saved to meta.json')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')


    try:
        # Send a GET request to the URL
        response = requests.get(url + '?action=getstream')
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the JSON content
        data = response.json()
        # Save the JSON data to a file
        with open('streams.json', 'w') as file:
            json.dump(data, file, indent=4)
            print('JSON data has been saved to streams.json')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    downloadData = downloadData()
