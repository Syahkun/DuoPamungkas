import json
from . import app, client, cache, create_token, init_database

class TestresepCrud():
    id_resep = 0

    def test_resep_id_invalid(self, client, init_database):
        token = create_token()
        res = client.get(
            '/resep/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_resep_id(self, client, init_database):
        token = create_token()
        res = client.get(
            '/resep/1', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200