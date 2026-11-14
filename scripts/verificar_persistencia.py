#!/usr/bin/env python3
"""Comprueba datos previos. --recrear reinicia SOLO el proyecto Kafka de este repo."""
import argparse,json,pathlib,subprocess,os,datetime
root=pathlib.Path(__file__).resolve().parents[1]; os.chdir(root)
p=argparse.ArgumentParser(); p.add_argument('--recrear',action='store_true'); args=p.parse_args()
if args.recrear:
 subprocess.run(['docker','compose','up','-d','--force-recreate','--wait','--wait-timeout','180'],check=True)
results=[]
for path in sorted((root/'experimento/resultados').glob('*/resumen.json')):
 summary=json.loads(path.read_text())
 if summary['status']!='PASS': continue
 for n,t in summary['topics'].items():
  cmd=['docker','compose','exec','-T','kafka1','/opt/kafka/bin/kafka-console-consumer.sh','--bootstrap-server','kafka1:9092','--topic',t['topic'],'--from-beginning','--timeout-ms','5000']
  r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=45)
  observed=[x for x in r.stdout.splitlines() if x.startswith(summary['run_utc']+'|')]
  ok=r.returncode==0 and sorted(observed)==sorted(t['mensajes'])
  results.append({'topic':t['topic'],'estado':'PASS' if ok else 'FAIL','esperados':t['observados'],'observados':len(observed),'command':cmd,'output':r.stdout,'exit_code':r.returncode})
  print(t['topic'],results[-1]['estado'],flush=True)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'recreacion_solicitada':args.recrear,'operador':'asistente-IA','resultados':results,'status':'PASS' if results and all(x['estado']=='PASS' for x in results) else 'FAIL'}
(root/'experimento/persistencia.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
raise SystemExit(0 if report['status']=='PASS' else 1)
