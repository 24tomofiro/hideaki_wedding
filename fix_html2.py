import codecs
text = codecs.open('index.html', 'r', 'utf-8').read()
text = text.replace('▼ tap to see profile', '<span class="arrow">▼</span> tap to see profile')
codecs.open('index.html', 'w', 'utf-8').write(text)
print('Done!')
