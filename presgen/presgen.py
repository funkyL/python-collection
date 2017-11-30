# Creates song slides presentation (*.fodp) file with data collected in xml file.
# Runs in command line. 

from xml.etree import ElementTree as ET

NS = {  "office" : "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        "draw" : "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
        "text" : "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
        "dc" : "http://purl.org/dc/elements/1.1/",
        "style" : "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
        "table" : "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "fo" : "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
        "xlink" :"http://www.w3.org/1999/xlink",
        "meta" : "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
        "number" : "urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0",
        "presentation" : "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
        "svg" : "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
        "chart" : "urn:oasis:names:tc:opendocument:xmlns:chart:1.0",
        "dr3d" : "urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0",
        "math" : "http://www.w3.org/1998/Math/MathML",
        "form" : "urn:oasis:names:tc:opendocument:xmlns:form:1.0",
        "script" : "urn:oasis:names:tc:opendocument:xmlns:script:1.0",
        "config" : "urn:oasis:names:tc:opendocument:xmlns:config:1.0",
        "ooo" : "http://openoffice.org/2004/office",
        "ooow" : "http://openoffice.org/2004/writer",
        "oooc" : "http://openoffice.org/2004/calc",
        "dom" : "http://www.w3.org/2001/xml-events",
        "xforms" : "http://www.w3.org/2002/xforms",
        "xsd" : "http://www.w3.org/2001/XMLSchema",
        "xsi" : "http://www.w3.org/2001/XMLSchema-instance",
        "smil" : "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0",
        "anim" : "urn:oasis:names:tc:opendocument:xmlns:animation:1.0",
        "rpt" : "http://openoffice.org/2005/report",
        "of" : "urn:oasis:names:tc:opendocument:xmlns:of:1.2",
        "xhtml" : "http://www.w3.org/1999/xhtml",
        "grddl" : "http://www.w3.org/2003/g/data-view#",
        "officeooo" : "http://openoffice.org/2009/office",
        "tableooo" : "http://openoffice.org/2009/table",
        "drawooo" : "http://openoffice.org/2010/draw",
        "calcext" : "urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0",
        "loext" : "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0",
        "field" : "urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0",
        "formx" : "urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0",
        "css3t" : "http://www.w3.org/TR/css3-text/",
        "office:version" : "1.2",
        "office:mimetype" : "application/vnd.oasis.opendocument.presentation",
        }


for name, uri in NS.items():
  ET.register_namespace(name, uri)


template_path = ('./lovsang.fodp')
template_root = ET.parse(template_path).getroot()
songlist_xml = ET.parse('./sange-sample.xml')
songlist = songlist_xml.findall('song')

preslist = []

def find(searchtext):
  print('\nResultater for s' + str(searchtext))
  for song in songlist:
    title = song.find('title').text
    result = 0
    for w in searchtext:
      w_present = title.casefold().find(w.casefold())
      if w_present != -1: result += 1
    if result == len(searchtext):
        print(song.attrib['id'] + ": " + title)

def add(song_ids):
  while(len(song_ids) > 0):
    song_id = song_ids.pop(0)
    for song in songlist:
      if song.attrib['id'] == str(song_id):
        preslist.append(song)
        break

def l():
  print('')
  for song in preslist:
    print(song.attrib['id'] + ": " + song.find('title').text)


class NewSlide:

  def __init__(self, output_file=None, template_file_path=None):
    self.template_file_path = "./lovsang.fodp"
    self.tree = ET.parse(self.template_file_path)

    self.root = self.tree.getroot()
    #self.__seperatePageElements()    #deprecated
    self.presentation = self.root.find("office:body", NS).find("office:presentation", NS)
    self.page_model = self.__setPageModel()
    self.pagecount = 1


  def __setPageModel(self):
    # Copy page model and detach

    page_model = self.presentation.find("draw:page", NS)
    page_model.attrib.pop("draw:name", None)
    page_model = ET.fromstring(ET.tostring(page_model))
    return page_model


  def createSlide(self, songlist):

    for song in songlist:
      title = song.find("title")
      lyrics = song.findall("lyrics")
      for verse in lyrics:
        self.__createPage(title, verse)
      self.presentation.append(self.page_model)
    self.__saveSlide()
    return

  def __createPage(self, title, verse):
    #create page object
    new_page = ET.fromstring(ET.tostring(self.page_model))
    lyrics_box = new_page.find("draw:frame", NS).find("draw:text-box", NS)
    line_vanilla = ET.tostring(lyrics_box.find("text:p", NS))
    lyrics_box.remove(lyrics_box.find("text:p", NS))

    # page ids, not working
    """
    self.pagecount += 1
    pagename = 'page'+ str(self.pagecount)
    new_page.set('draw:name', pagename)"""

    for line in verse.text.splitlines():
      new_line = ET.fromstring(line_vanilla)
      new_line.find("text:span", NS).text = line
      lyrics_box.append(new_line)

    new_page[1][0][0].text = title.text
    self.presentation.append(new_page)
    return


  def __saveSlide(self):
    self.tree.write('./output.fodp',
      xml_declaration=True,
      encoding='utf-8',
      method='xml')


#######################################################################

if __name__ == "__main__":
  """ midlertidig test or generate start"""
  message = "Commands: (f)ind, (a)dd, (l)ist, (s)ave, e(x)it"
  print(message)


  """ / midleridig test for generate slut"""
  while 1:
    q = str(input('>>')).split()
    if len(q) > 0:
      qc = q.pop(0)
      if qc == 'find' or qc == 'f':
        find(q)

      elif qc == 'add' or qc == 'a':
        add(q)

      elif qc == 'list' or qc == 'l':
        l()

      elif qc == 'save' or qc == 's':
        NewSlide().createSlide(preslist)

      elif qc == 'exit' or qc == 'x':
        break

      else: print('Unknown request.');
