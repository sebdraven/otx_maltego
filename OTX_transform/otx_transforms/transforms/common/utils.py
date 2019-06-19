from canari.maltego.entities import IPv4Address, Domain, URL, Hash

gram = {
'maltego.Domain':'hostname',
'maltego.IPv4Address': 'IPv4'
}

cores = {
    'IPv4': IPv4Address,
    'domain': Domain,
    'hostname': Domain,
    'URL':  URL,
    'FileHash-MD5': Hash,
    'FileHash-SHA1': Hash,
    'FileHash-SHA256': Hash,
}