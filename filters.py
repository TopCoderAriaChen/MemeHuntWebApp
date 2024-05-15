import hashlib

def email_hash(email):
  return hashlib.md5(email.lower().encode("utf-8")).hexdigest()

if __name__== "__main__":
  myemail="yggl1889@163.com"
  print(email_hash(myemail))