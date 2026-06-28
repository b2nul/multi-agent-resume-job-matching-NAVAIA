from navaia_forge import NavaiaForgeClient

client = NavaiaForgeClient(base_url="http://localhost:8001")

pair = client.auth.login(
    email="bayan@gmail.com",          # same email you used before
    password="choose-a-strong-password",  # same password you used before
)

print("ACCESS TOKEN:", repr(pair.access_token))

authed = NavaiaForgeClient(base_url="http://localhost:8001/api/v1", api_key=pair.access_token)
key = authed.auth.create_key("my-key")
print("LOCAL API KEY:", key.api_key)