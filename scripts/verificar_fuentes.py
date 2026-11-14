#!/usr/bin/env python3
"""Coteja metadatos completos y destino DOI; separa acceso editorial de identidad bibliográfica."""
import datetime,json,pathlib,re,sys,unicodedata,urllib.request,urllib.error,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
HEADERS={'User-Agent':'Mozilla/5.0 (TA-IND-01 bibliographic verification)'}
def norm(value):
 return ''.join(c for c in unicodedata.normalize('NFKD',str(value).lower()) if c.isalnum())
def target(value):
 parsed=urllib.parse.urlsplit(value); return (parsed.hostname or '').lower(),urllib.parse.unquote(parsed.path).rstrip('/').lower()
class NoFollow(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs): return None
opener=urllib.request.build_opener(NoFollow())
report={'fecha_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fuentes':[]}
bib=(ROOT/'informe/referencias.bib').read_text()
for kind,key,body in re.findall(r'@(\w+)\{([^,]+),(.*?)(?=\n@|\Z)',bib,re.S):
 fields=dict(re.findall(r'^\s*(\w+)\s*=\s*\{(.*)\}\s*,?\s*$',body,re.M))
 if 'doi' not in fields: continue
 item={'clave':key,'doi':fields['doi'],'tipo_bib':kind,'estado':'PENDIENTE','discrepancias':[]}
 try:
  req=urllib.request.Request('https://api.crossref.org/works/'+fields['doi'],headers=HEADERS)
  with urllib.request.urlopen(req,timeout=30) as response: message=json.load(response)['message']
  item['crossref']=message
  checks={'doi':(fields['doi'],message.get('DOI','')),
   'title':(fields.get('title',''),message.get('title',[''])[0]),
   'publication':(fields.get('journaltitle',fields.get('booktitle','')),message.get('container-title',[''])[0]),
   'volume':(fields.get('volume',''),message.get('volume','')),
   'issue':(fields.get('number',''),message.get('issue','')),
   'pages_or_eid':(fields.get('pages',fields.get('eid','')),message.get('page',message.get('article-number',''))),
   'type':('journal-article' if kind=='article' else 'proceedings-article',message.get('type',''))}
  for name,(expected,actual) in checks.items():
   if norm(expected)!=norm(actual): item['discrepancias'].append({'campo':name,'bib':expected,'crossref':actual})
  expected_auth=[norm(a) for a in fields.get('author','').split(' and ')]
  actual_auth=[norm(a.get('family','')+', '+a.get('given','')) for a in message.get('author',[])]
  if expected_auth!=actual_auth: item['discrepancias'].append({'campo':'autores_completos_y_orden','bib':expected_auth,'crossref':actual_auth})
  published=next((message[k]['date-parts'][0] for k in ['published-print','issued','published','published-online'] if message.get(k,{}).get('date-parts')),[])
  year=fields.get('date',fields.get('year',''))[:4]
  if not published or year!=str(published[0]): item['discrepancias'].append({'campo':'año_publicación','bib':year,'crossref':published})
  item['metadatos']='COINCIDEN' if not item['discrepancias'] else 'DISCREPANCIAS'
  # Leer la redirección sin perder su prueba cuando la editorial limita robots.
  req=urllib.request.Request('https://doi.org/'+fields['doi'],headers=HEADERS)
  try:
   with opener.open(req,timeout=30) as response:
    status=response.status; destination=response.url
  except urllib.error.HTTPError as error:
   if error.code not in [301,302,303,307,308]: raise
   status=error.code; destination=urllib.parse.urljoin(req.full_url,error.headers['Location'])
  item['resolucion_doi']={'http':status,'destino':destination}
  registered=message.get('resource',{}).get('primary',{}).get('URL','')
  item['destino_editorial_registrado']=registered
  item['destino_coincide_registro']=bool(registered) and target(destination)==target(registered)
  if not item['destino_coincide_registro']: item['discrepancias'].append({'campo':'destino_doi','doi':destination,'crossref':registered})
  # Este acceso se informa aparte: un 403 editorial no borra el cotejo anterior.
  try:
   with urllib.request.urlopen(urllib.request.Request(destination,headers=HEADERS),timeout=30) as response:
    item['acceso_editorial']={'http':response.status,'url_final':response.url,'tipo_contenido':response.headers.get('Content-Type')}
  except (urllib.error.URLError,TimeoutError) as error:
   item['acceso_editorial']={'estado':'LIMITADO','error':str(error)}
  item['estado']='REVISAR_DISCREPANCIAS' if item['discrepancias'] else 'METADATOS_Y_REDIRECCION_OK'
 except (urllib.error.URLError,TimeoutError,KeyError,ValueError) as error:
  item['error']=str(error); item['estado']='BLOQUEADO_O_INCOMPLETO'
 report['fuentes'].append(item); print(key,item['estado'],flush=True)
report['nota']='OK acredita cotejo de nombres y orden, título, publicación, tipo, volumen, fascículo, páginas/eid, año y destino DOI registrado. No acredita acceso integral, lectura personal, indexación ni la validez de cada afirmación del informe. Una respuesta editorial 202 tampoco prueba lectura del artículo.'
(ROOT/'fuentes/verificacion-doi.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
sys.exit(0 if report['fuentes'] and all(x['estado']=='METADATOS_Y_REDIRECCION_OK' for x in report['fuentes']) else 1)
