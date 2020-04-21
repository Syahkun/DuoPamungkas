import json
from . import app, client, cache, create_token, init_database

class TestClientCrud():
    def test_client_list(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_client_insert(self, client, init_database):
        token = create_token()

        data = {
            "client_key": "clienthehe",
            "client_secret": "rahasiaaaa",
            "status": "True"
        }

        res = client.post(
            '/client', 
            json = data,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_id(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client/1', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_id_invalid(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_client_update(self, client, init_database):
        token = create_token()

        data = {
            "client_key": "clientheh0",
            "client_secret": "rahasiaayaa",
            "status": "True"
        }

        res = client.put(
            '/client/1', 
            json = data,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_client_update_invalid(self, client, init_database):
        token = create_token()

        data = {
            "client_key": "clientheh0",
            "client_secret": "rahasiaayaa",
            "status": "True"
        }

        res = client.put(
            '/client/100', 
            json = data,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404


    def test_client_remove(self, client, init_database):
        token = create_token()
        res = client.delete(
            '/client/1', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_client_remove_invalid(self, client, init_database):
        token = create_token()
        res = client.delete(
            '/client/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_get_filterby(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client', 
            query_string={
                "id": 1,
                "status": "true",
                "orderby": "id",
                "sort": "desc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby2(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client', 
            query_string={
                "id": 1,
                "status": "false",
                "orderby": "id",
                "sort": "asc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby3(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client', 
            query_string={
                "id": 1,
                "status": "true",
                "orderby": "status",
                "sort": "desc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby4(self, client, init_database):
        token = create_token()
        res = client.get(
            '/client', 
            query_string={
                "id": 1,
                "status": "true",
                "orderby": "status",
                "sort": "asc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200