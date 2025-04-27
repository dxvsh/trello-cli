from typing import Dict, List
import requests

class TrelloAPI:
    BASE_URL = "https://api.trello.com/1"
    
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.auth_params = {
            'key': self.api_key,
            'token': self.token
        }

    def get_boards(self) -> List[Dict[str, str]]:
        """Retrieve all boards for the authenticated user."""
        url = f"{self.BASE_URL}/members/me/boards"
        params = {
            **self.auth_params,
            # we just want the name and id of the user's boards
            'fields': 'name,id'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return [
            {
                'name': board['name'], 
                'id': board['id']
            } for board in response.json()
        ]

    def get_lists_in_board(self, board_id: str) -> List[Dict[str, str]]:
        """Retrieve all lists in a specific board."""
        url = f"{self.BASE_URL}/boards/{board_id}/lists"
        params = {
            **self.auth_params,
            # only returns the name and id of the lists in the specified board
            'fields': 'name,id'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return [
            {
                'name': lst['name'], 
                'id': lst['id']
            } for lst in response.json()
        ]

    def get_labels_in_board(self, board_id: str) -> List[Dict[str, str]]:
        """Retrieve all labels in a specific board."""
        url = f"{self.BASE_URL}/boards/{board_id}/labels"
        params = {
            **self.auth_params,
            # we want the name, id and color for each label in this board
            'fields': 'name,id,color'  
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return [
            {
                # label names can also be empty strings (''), and color can be NoneType
                'name': label['name'] if label['name'] else 'Unnamed Label',
                'id': label['id'],
                'color': label['color'] if label['color'] else 'No Color'
            } for label in response.json()
        ]
    
    def search_cards(self, query: str) -> List[Dict[str, str]]:
        """Search for cards using a query string across all your boards"""
        url = f"{self.BASE_URL}/search"

        params = {
            **self.auth_params,
            'query': query,
            'modelTypes': 'cards', # only search for cards,
            'card_fields': 'name,shortUrl'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return [
            {
                'id': card['id'],
                'name': card['name'],
                'shortUrl': card['shortUrl']
            } for card in response.json()['cards']
        ]

    def create_card(self, list_id: str, name: str, labels: list[str] = None, comment: str = None) -> dict:
        """Create a new card in the specified list."""
        url = f"{self.BASE_URL}/cards"
        
        params = {
            **self.auth_params,
            'idList': list_id,
            'name': name,
        }
        
        # if a list of lable ids is given, make sure to convert it
        # into a string of comma separated values, so we can use 
        # them in the API call for adding labels to our card
        if labels:
            params['idLabels'] = ','.join(labels)
            
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        card = response.json()
        
        # Add comment if provided
        if comment and card.get('id'):
            self.add_comment(card['id'], comment)
            
        return card
    
    def add_comment(self, card_id: str, comment: str) -> dict:
        """Add a comment to a card."""
        url = f"{self.BASE_URL}/cards/{card_id}/actions/comments"
        params = {
            **self.auth_params,
            'text': comment
        }
        
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()