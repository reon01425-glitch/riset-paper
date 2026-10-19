import re,zipfile,shutil,sys
src,dst=sys.argv[1],sys.argv[2]
zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    d=zin.read(it.filename)
    if it.filename=='word/document.xml':
        x=d.decode('utf8')
        # full-width tables, autofit columns
        x=re.sub(r'<w:tblW [^>]*/>','<w:tblW w:w="5000" w:type="pct"/>',x)
        x=re.sub(r'<w:tblLayout [^>]*/>','<w:tblLayout w:type="autofit"/>',x)
        # paragraphs inside table cells: compact, no extra spacing, 8.5 pt
        def cell(m):
            c=m.group(0)
            c=re.sub(r'(<w:pPr>(?:<w:pStyle [^>]*/>)?)',r'\1<w:spacing w:before="0" w:after="0"/>',c)
            return c
        x=re.sub(r'<w:tc>.*?</w:tc>',cell,x,flags=re.S)
        d=x.encode('utf8')
    elif it.filename=='[Content_Types].xml':
        x=d.decode('utf8')
        if 'Extension="png"' not in x:
            x=x.replace('<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="png" ContentType="image/png"/>')
        d=x.encode('utf8')
    elif it.filename=='word/numbering.xml':
        x=d.decode('utf8')
        x=re.sub(r'<w:nsid w:val="([0-9A-Fa-f]+)"',lambda m:'<w:nsid w:val="%s"'%m.group(1).rjust(8,'0')[-8:],x)
        d=x.encode('utf8')
    elif it.filename=='word/settings.xml':
        x=re.sub(r'<w:zoom [^>]*/>','',d.decode('utf8'))
        d=x.encode('utf8')
    zout.writestr(it,d)
zout.close()
