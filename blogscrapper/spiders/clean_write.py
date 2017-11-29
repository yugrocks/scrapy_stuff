def clean_write(string, file):
    for _ in string:
      asc = ord(_)
      if asc!=12 and asc!=7 and asc < 128: 
          file.write(_)
      else:
          file.write(" ")
