path = r"C:\Python310\lib\site-packages\navaia_forge\resources\auth.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the stray "test" line we accidentally appended earlier
content = content.replace("\ntest\n", "\n")
content = content.replace("\ntest", "")

# Patch create_key to send Authorization: Bearer explicitly
old = '            self._http.post("/auth/keys", {"name": name}),'
new = '            self._http.post("/auth/keys", {"name": name}, headers={"Authorization": f"Bearer {self._http.api_key}"}),'

if old in content:
    content = content.replace(old, new)
    print("Patched create_key successfully.")
else:
    print("WARNING: old create_key line not found — file may already be patched or differ from expected.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done writing file.")