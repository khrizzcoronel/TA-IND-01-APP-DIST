#!/usr/bin/env python3
"""Cotejo DOI/Crossref. Un bloqueo nunca se registra como verificación válida."""
import datetime,json,pathlib,re,sys,unicodedata,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
bib=(ROOT/'informe/referencias.bib').read_text()
def norm(t): return ''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if c.isalnum())
report={'fecha_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fuentes':[]}
for kind,key,body in re.findall(r'@(\w+)\{([^,]+),(.*?)(?=\n@|\Z)',bib,re.S):
 fields=dict(re.findall(r'^\s*(\w+)\s*=\s*\{(.*)\}\s*,?\s*$',body,re.M))
 if 'doi' not in fields: continue
 item={'clave':key,'doi':fields['doi'],'estado':'PENDIENTE','discrepancias':[]}
 try:
  req=urllib.request.Request('https://api.crossref.org/works/'+fields['doi'],headers={'User-Agent':'TA-IND-01 bibliographic verification'})
  with urllib.request.urlopen(req,timeout=25) as response: message=json.load(response)['message']
  item['crossref']=message
  checks={'title':(fields.get('title',''),message.get('title',[''])[0]),
   'publication':(fields.get('journaltitle',fields.get('booktitle','')),message.get('container-title',[''])[0]),
   'volume':(fields.get('volume',''),message.get('volume','')),
   'pages_or_eid':(fields.get('pages',fields.get('eid','')),message.get('page',message.get('article-number','')))}
  for name,(expected,actual) in checks.items():
   if expected and norm(expected)!=norm(str(actual)): item['discrepancias'].append({'campo':name,'bib':expected,'crossref':actual})
  expected_auth=[norm(a.split(',')[0]) for a in fields.get('author','').split(' and ')]
  actual_auth=[norm(a.get('family','')) for a in message.get('author',[])]
  if expected_auth!=actual_auth: item['discrepancias'].append({'campo':'autores','bib':expected_auth,'crossref':actual_auth})
  years={str(message[k]['date-parts'][0][0]) for k in ['published','published-print','published-online','issued'] if k in message}
  year=fields.get('date',fields.get('year',''))[:4]
  if year not in years: item['discrepancias'].append({'campo':'año','bib':year,'crossref':sorted(years)})
  # Se verifica que el DOI resuelva, además de consultar el registro.
  with urllib.request.urlopen(urllib.request.Request('https://doi.org/'+fields['doi'],headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as response:
   item['destino_doi']=response.url; item['http_destino']=response.status
  item['estado']='REVISAR_DISCREPANCIAS' if item['discrepancias'] else 'METADATOS_Y_RESOLUCION_OK_REQUIERE_LECTURA'
 except (urllib.error.URLError,TimeoutError,KeyError,ValueError) as e:
  item['error']=str(e); item['estado']='BLOQUEADO_O_INCOMPLETO'
 report['fuentes'].append(item)
 print(key,item['estado'])
report['nota']='Este cotejo automático no sustituye comprobar fascículo, nombre completo de autores, indexación, lectura y correspondencia de cada cita con el artículo.'
(ROOT/'fuentes/verificacion-doi.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
sys.exit(0 if all(x['estado']=='METADATOS_Y_RESOLUCION_OK_REQUIERE_LECTURA' for x in report['fuentes']) else 1)
