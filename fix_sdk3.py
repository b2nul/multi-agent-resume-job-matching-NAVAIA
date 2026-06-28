path = r"C:\Python310\lib\site-packages\navaia_forge\resources\auth.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the corrupted trailing "t e s t" debris and any blank lines after it
idx = content.find("t e s t")
if idx != -1:
    content = content[:idx].rstrip() + "\n"
    print("Removed corrupted trailing test debris.")
else:
    print("No 't e s t' debris found — already clean.")

# Now patch create_key to send Authorization: Bearer explicitly
old = '            self._http.post("/auth/keys", {"name": name}),'
new = '            self._http.post("/auth/keys", {"name": name}, headers={"Authorization": f"Bearer {self._http.api_key}"}),'

if new in content:
    print("create_key already patched.")
elif old in content:
    content = content.replace(old, new)
    print("Patched create_key successfully.")
else:
    print("WARNING: expected create_key line not found at all.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("File rewritten. New size will differ from 3711 bytes.")