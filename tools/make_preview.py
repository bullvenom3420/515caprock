"""Turn index.html into an artifact page (the artifact host supplies doctype/charset/viewport)."""
import re
s = open('/home/claude/515caprock/index.html').read()
head = s.split('<head>')[1].split('</head>')[0]
body = s.split('<body>')[1].split('</body>')[0] if '<body>' in s else s.split('</head>')[1]
head = re.sub(r'<meta charset[^>]*>\s*', '', head)
head = re.sub(r'<meta name="viewport"[^>]*>\s*', '', head)
head = re.sub(r'<title>[^<]*</title>\s*', '', head)
open('/home/claude/515caprock/preview.html', 'w').write('<title>515 Cap Rock Drive</title>\n' + head + body)
print('ok')
