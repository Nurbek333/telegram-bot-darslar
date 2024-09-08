import wikipedia

wikipedia.set_lang("uz")

print(wikipedia.search('Tashkent'))
print(wikipedia.summary('Navoiy'))
print(wikipedia.summary('Samarqand'))
print(wikipedia.summary('Fargana'))
print(wikipedia.summary('Buhoro'))