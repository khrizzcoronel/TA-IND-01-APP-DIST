#!/usr/bin/env python3
"""Comprobaciones de archivos; no acredita autoría, indexación ni entrega en SGA."""
import datetime,json,pathlib,re,shutil,subprocess,sys,tempfile,xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def add(name,state,detail): checks.append({'comprobacion':name,'estado':state,'detalle':detail})
def pdf_pages(file):
 text=subprocess.check_output(['pdfinfo',str(file)],text=True)
 return int(re.search(r'^Pages:\s+(\d+)',text,re.M)[1])
for executable in ['pdfinfo','pdftotext','git']:
 if not shutil.which(executable):
  print(f'Falta {executable}; instala Poppler y Git antes de ejecutar el control.'); sys.exit(1)
try:
 sga=ROOT/'entrega-sga.pdf'; count=pdf_pages(sga)
 add('PDF SGA de una página','PASS' if count==1 else 'FAIL',f'{count} página(s)')
 with tempfile.TemporaryDirectory(prefix='ta-ind-pdf-') as temp:
  xml=pathlib.Path(temp)/'sga.xml'; subprocess.run(['pdftotext','-bbox',str(sga),str(xml)],check=True)
  matches=[x for x in ET.parse(xml).iter() if x.tag.endswith('word') and (x.text or '').startswith('https://github.com/')]
  expected='https://github.com/khrizzcoronel/TA-IND-01-APP-DIST'
  add('URL SGA íntegra en una línea','PASS' if len(matches)==1 and matches[0].text==expected else 'FAIL','Se comprueba un único elemento de texto con la URL completa.')
 report_pdf=ROOT/'informe/main.pdf'; n=pdf_pages(report_pdf)
 text=subprocess.check_output(['pdftotext','-layout',str(report_pdf),'-'],text=True)
 pages=text.split('\f'); ref=next((i+1 for i,p in enumerate(pages) if re.search(r'^\s*Referencias\s*$',p,re.M)),None)
 full_body_pages=max(0,ref-2) if ref else 0
 add('Extensión de contenido','PASS' if full_body_pages>=5 else 'FAIL',f'{n} páginas totales; {full_body_pages} páginas completas entre carátula y comienzo de referencias. No se cuentan referencias ni anexos.')
 source=(ROOT/'informe/main.tex').read_text(); abstract=source.split('\\section*{Resumen}')[1].split('\\section{')[0]
 words=len(abstract.split()); add('Resumen entre 150 y 200 palabras','PASS' if 150<=words<=200 else 'FAIL',f'{words} palabras por separación de espacios.')
 add('Bibliografía con Biber e IEEE','PASS' if re.search(r'backend=biber',source) and re.search(r'style=ieee',source) else 'FAIL','Comprobación de configuración LaTeX; no verifica metadatos ni calidad de citas.')
 bib=(ROOT/'informe/referencias.bib').read_text(); entries={key:kind.lower() for kind,key in re.findall(r'@(\w+)\{([^,]+),',bib)}
 cited={key.strip() for group in re.findall(r'\\(?:cite|fullcite)\{([^}]+)\}',source) for key in group.split(',')}
 missing=sorted(cited-set(entries)); add('Claves de cita existentes','FAIL' if missing else 'PASS',missing or 'Todas las claves citadas existen en el .bib.')
 add('Cantidad de fuentes citadas','PASS' if len(cited)>=6 else 'FAIL',f'{len(cited)} claves distintas citadas; este conteo no acredita veracidad.')
 articles=[key for key in cited if entries.get(key)=='article']; add('Tres artículos candidatos de revista','PASS' if len(articles)>=3 else 'FAIL',{'cantidad':len(articles),'claves':sorted(articles),'limite':'Tipo declarado en BibLaTeX. Indexación, DOI y lectura requieren verificación adicional.'})
 doi=json.loads((ROOT/'fuentes/verificacion-doi.json').read_text()); records=doi.get('fuentes',[])
 good=bool(records) and all(x['estado'] in ['METADATOS_Y_RESOLUCION_OK_REQUIERE_LECTURA','METADATOS_Y_REDIRECCION_OK'] for x in records)
 add('Verificación de DOI','PASS' if good else 'PENDIENTE',[{'clave':x['clave'],'estado':x['estado']} for x in records])
 index=json.loads((ROOT/'fuentes/indexacion.json').read_text()).get('revistas',[])
 add('Indexación corroborada de tres revistas','PASS' if len(index)>=3 and all(x['estado']=='CORROBORADA' for x in index) else 'PENDIENTE',{'revistas':[x['revista'] for x in index],'limite':'IEEE: editorial; dos Elsevier: fuente secundaria SCImago basada en Scopus. No acredita lectura personal.'})
 for folder,minimum,label in [('ejecucion',4,'Capturas de ejecución'),('lecturas',3,'Capturas de artículos anotados'),('bosquejo',1,'Fotografía del bosquejo')]:
  files=[p.relative_to(ROOT).as_posix() for p in (ROOT/'evidencia'/folder).glob('**/*') if p.is_file() and p.suffix.lower() in ['.png','.jpg','.jpeg','.webp']]
  add(label,'PASS' if len(files)>=minimum else 'PENDIENTE',{'archivos_presentes':len(files),'mínimo':minimum,'archivos':files,'limite':'La presencia de imágenes no prueba originalidad ni autoría; hace falta revisión personal.'})
 personal_runs=[]
 for file in (ROOT/'experimento/resultados').glob('*/resumen.json'):
  run=json.loads(file.read_text())
  if run.get('operador')=='estudiante' and run.get('status')=='PASS': personal_runs.append(file.parent.name)
 add('Ejecución personal registrada','PASS' if personal_runs else 'PENDIENTE',{'corridas_declaradas_estudiante':personal_runs,'limite':'La etiqueta de operador no acredita por sí sola autoría personal.'})
 history=subprocess.check_output(['git','log','--format=%aI'],cwd=ROOT,text=True).splitlines()
 days={datetime.datetime.fromisoformat(x).astimezone(ZoneInfo('America/Guayaquil')).date().isoformat() for x in history}
 add('Historial progresivo','PASS' if len(history)>=8 and len(days)>=3 else 'PENDIENTE',{'commits_totales':len(history),'días_locales':sorted(days),'limite':'Se necesitan al menos ocho commits en tres días y verificar autoría real del estudiante; no se reescribe el historial.'})
 pending=re.findall(r'^- \[ \] (.+)$',(ROOT/'PENDIENTES.md').read_text(),re.M)
 add('Revisión de requisitos restantes','PENDIENTE' if pending else 'PASS',pending)
except (OSError,subprocess.CalledProcessError,ValueError,KeyError,IndexError,ET.ParseError) as error:
 add('Ejecución de comprobaciones','FAIL',str(error))
status='NO_LISTO_PARA_ENTREGA' if any(x['estado']!='PASS' for x in checks) else 'REQUIERE_CONFIRMACION_HUMANA_FINAL'
result={'fecha_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'estado':status,'advertencia':'Este control no acredita autoría, lectura, indexación, acceso público actual, video, permisos ni entrega en SGA. No sustituye la revisión del docente.','comprobaciones':checks}
(ROOT/'revision-entrega.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for x in checks: print(f"{x['estado']}: {x['comprobacion']}")
print(status)
sys.exit(2 if status=='NO_LISTO_PARA_ENTREGA' else 0)
