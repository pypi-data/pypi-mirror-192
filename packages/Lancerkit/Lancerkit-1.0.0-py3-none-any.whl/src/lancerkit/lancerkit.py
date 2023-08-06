HOST = 'https://api.lancerkit.com'
import requests
import json

class Lancerkit: 
    def __init__(self, api_key): 
        self.api_key = api_key

    def list_documents(self, page=1, sort='-date'): 
        return requests.get(f"{HOST}/documents?sort={sort}&page={page}", headers={"authorization": self.api_key})

    def list_contacts(self, page=1, sort='-date'): 
        return requests.get(f"{HOST}/contacts?sort={sort}&page={page}", headers={"authorization": self.api_key})

    def list_transactions(self, page=1, sort='-date'): 
        return requests.get(f"{HOST}/transactions?sort={sort}&page={page}", headers={"authorization": self.api_key})

    def create_document(self, data): 
        self.edit_document('new', data)

    def create_contact(self, data): 
        self.edit_contact('new', data) 

    def edit_transaction(self, id, data): 
        return requests.post(f"{HOST}/transactions/{id}", data=json.dumps(data), headers={"Content-Type": "application/json", "authorization": self.api_key})

    def edit_document(self, id, data): 
        return requests.post(f"{HOST}/documents/{id}", data=json.dumps(data), headers={"Content-Type": "application/json", "authorization": self.api_key})

    def edit_contact(self, id, data): 
        return requests.post(f"{HOST}/contacts/{id}", data=json.dumps(data), headers={"Content-Type": "application/json", "authorization": self.api_key})

    def delete_transaction(self, ids): 
        return requests.post(f"{HOST}/transactions/delete", data=json.dumps(ids), headers={"Content-Type": "application/json", "authorization": self.api_key})

    def delete_document(self, ids): 
        return requests.post(f"{HOST}/documents/delete", data=json.dumps(ids), headers={"Content-Type": "application/json", "authorization": self.api_key})

    def delete_contact(self, ids): 
        return requests.post(f"{HOST}/contacts/delete", data=json.dumps(ids), headers={"Content-Type": "application/json", "authorization": self.api_key})
