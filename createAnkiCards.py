# import requests
# import json

# def invoke(action, **params):
#     return requests.post('http://localhost:8765', json={
#         'action': action,
#         'version': 6,
#         'params': params
#     }).json()

# def create_deck(deck_name):
#     invoke('createDeck', deck=deck_name)

# def add_note_to_deck(deck_name, question, answer):
#     note = {
#         'deckName': deck_name,
#         'modelName': 'Basic',
#         'fields': {
#             'Front': question,
#             'Back': answer
#         },
#         'tags': []
#     }
#     invoke('addNote', note=note)

# # デッキ名、問題、回答のリスト
# cards = [
#     {'deck': 'デッキ1', 'question': '問題1', 'answer': '回答1'},
#     {'deck': 'デッキ2', 'question': '問題2', 'answer': '回答2'},
#     # 必要に応じて追加
# ]

# for card in cards:
#     create_deck(card['deck'])
#     add_note_to_deck(card['deck'], card['question'], card['answer'])
