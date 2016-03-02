string = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;"></textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>

"""

def converter(a_string):
	for (i, o) in (('&', '&amp;'),
					('<','&lt;'),
					('>','&gt;'),
					('"','&quot;')):
		a_string = a_string.replace(i,o)

	return a_string

print converter(string)