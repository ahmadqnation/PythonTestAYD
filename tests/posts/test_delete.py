from helpers.api_client import delete

def test_slet_post():
    response = delete("/posts/1")
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 200

def test_slet_post_der_ikke_findes():
    response = delete("/posts/99999")
    print(f"\nResponse status: {response.status_code}")
    # JSONPlaceholder returnerer 200 selv for ikke-eksisterende ressourcer
    assert response.status_code == 200

def test_slet_sidste_gyldige_post():
    response = delete("/posts/100")
    assert response.status_code == 200

def test_slet_post_med_negativt_id():
    response = delete("/posts/-1")
    assert response.status_code == 200

def test_slet_post_med_tekst_som_id():
    response = delete("/posts/abc")
    assert response.status_code == 200

def test_valider_tomt_response():
    response = delete("/posts/1")
    assert response.status_code == 200
    assert response.json() == {}
