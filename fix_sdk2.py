path = r"C:\Python310\lib\site-packages\navaia_forge\resources\auth.py"

with open(path, "rb") as f:
    raw = f.read()

print("File size:", len(raw))
print("First 20 bytes:", raw[:20])
print("Last 100 bytes:", raw[-100:])