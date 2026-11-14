#!/usr/bin/env python3
"""Prueba real de Kafka. No produce capturas ni atribuye autoría al estudiante."""
import argparse, datetime as dt, getpass, json, os, pathlib, re, shlex, socket, subprocess, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
os.chdir(ROOT)
p=argparse.ArgumentParser(); p.add_argument('--operador',required=True,choices=['asistente-IA','estudiante']); p.add_argument('--pausas',action='store_true',help='Pausar para capturar cada fase de una sesión personal'); args=p.parse_args()
stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
folder=ROOT/'experimento'/'resultados'/stamp; folder.mkdir(parents=True)
log=(folder/'terminal.log').open('w'); records=[]

def pause(phase):
    print(f'FASE: {phase} | UTC: {dt.datetime.now(dt.timezone.utc).isoformat()} | usuario: {getpass.getuser()} | host: {socket.gethostname()}',flush=True)
    if args.pausas: input('Obtén tu captura original y pulsa Enter para continuar: ')

def run(cmd, data=None, timeout=100):
    line='$ '+shlex.join(cmd)+'\n'; print(line,flush=True); log.write(line)
    if data: log.write('ENTRADA:\n'+data+'\n')
    start=time.monotonic()
    r=subprocess.run(cmd,input=data,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    seconds=round(time.monotonic()-start,3)
    print(r.stdout,flush=True)
    log.write(r.stdout+f'\n[exit={r.returncode}; segundos={seconds}]\n'); log.flush()
    records.append({'command':cmd,'stdin':data,'exit_code':r.returncode,'seconds':seconds,'output':r.stdout})
    if r.returncode: raise RuntimeError(f'Comando falló: {r.stdout[-1500:]}')
    return r.stdout

def cli(service,script,*params,data=None):
    return run(['docker','compose','exec','-T',service,'/opt/kafka/bin/'+script,*params],data)

def describe(topic,service):
    return cli(service,'kafka-topics.sh','--bootstrap-server',service+':9092','--describe','--topic',topic)

def wait_isr(topic,service,n):
    deadline=time.monotonic()+150
    while time.monotonic()<deadline:
        text=describe(topic,service)
        m=re.search(r'Leader:\s*(\d+).*?Isr:\s*([\d,]+)',text)
        if m and len(m[2].split(','))==n: return int(m[1])
        time.sleep(3)
    raise RuntimeError(f'No se alcanzó ISR={n}')

def send(topic,service,phase):
    values=[f'{stamp}|{phase}|{i:02d}' for i in range(10)]
    text=cli(service,'kafka-console-producer.sh','--bootstrap-server',service+':9092','--topic',topic,
       '--producer-property','acks=all','--producer-property','enable.idempotence=true',
       '--producer-property','delivery.timeout.ms=10000','--producer-property','request.timeout.ms=5000',
       '--producer-property','max.block.ms=10000',data='\n'.join(values)+'\n')
    return values,text

summary={'run_utc':stamp,'operador':args.operador,'usuario_maquina':getpass.getuser(),'host':socket.gethostname(),
 'advertencia':'Validación asistida por IA; no es evidencia de ejecución personal del estudiante.' if args.operador=='asistente-IA' else 'Identidad y capturas personales deben acreditarse por separado.',
 'version':'Apache Kafka 3.9.1','factor_replicacion':3,'acks':'all','topics':{},'status':'FAIL'}
stopped=None
try:
    run(['docker','compose','up','-d','--wait','--wait-timeout','180'],timeout=210)
    names={2:'ta-isr2-'+stamp.lower(),3:'ta-isr3-'+stamp.lower()}
    expected={}
    for n,topic in names.items():
        cli('kafka1','kafka-topics.sh','--bootstrap-server','kafka1:9092','--create','--topic',topic,
            '--partitions','1','--replication-factor','3','--config',f'min.insync.replicas={n}',
            '--config','unclean.leader.election.enable=false')
        wait_isr(topic,'kafka1',3)
        values,text=send(topic,'kafka1','base')
        if 'ERROR' in text: raise RuntimeError(text)
        expected[n]=values
    pause('BASE: tres ISR y publicación inicial completada')
    leader=wait_isr(names[2],'kafka1',3)
    stopped=f'kafka{leader}'; survivor=next(f'kafka{i}' for i in range(1,4) if i!=leader)
    summary['broker_detenido']=stopped
    run(['docker','compose','stop',stopped])
    for n,topic in names.items(): wait_isr(topic,survivor,2)
    pause('FALLO: broker detenido; dos ISR')
    for n,topic in names.items():
        values,text=send(topic,survivor,'durante-fallo')
        if n==2:
            if 'ERROR' in text: raise RuntimeError(text)
            expected[n]+=values
        else:
            # La CLI puede terminar con exit=0 aunque no entregue mensajes.
            if 'NotEnoughReplicas' not in text: raise RuntimeError('Falta rechazo explícito por ISR insuficiente')
            summary['rechazo_isr3']='NotEnoughReplicasException observado; no se usa exit=0 como prueba de entrega'
    pause('CONTRASTE: ISR2 acepta; ISR3 rechaza')
    run(['docker','compose','start',stopped]); stopped=None
    for n,topic in names.items():
        wait_isr(topic,survivor,3)
        values,text=send(topic,survivor,'recuperacion')
        if 'ERROR' in text: raise RuntimeError(text)
        expected[n]+=values
        text=cli(survivor,'kafka-console-consumer.sh','--bootstrap-server',survivor+':9092',
            '--topic',topic,'--from-beginning','--timeout-ms','15000')
        observed=[line for line in text.splitlines() if line.startswith(stamp+'|')]
        if sorted(observed)!=sorted(expected[n]):
            raise RuntimeError(f'Mensajes inesperados/perdidos/duplicados: {topic}: {observed}')
        summary['topics'][str(n)]={'topic':topic,'esperados':len(expected[n]),'observados':len(observed),
            'conjunto_y_multiplicidad_correctos':True,'mensajes':observed}
    pause('RECUPERACIÓN: tres ISR y conjuntos de mensajes comprobados')
    summary['status']='PASS'
finally:
    if stopped: run(['docker','compose','start',stopped])
    (folder/'comandos.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    (folder/'resumen.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    log.close()
    print(json.dumps(summary,indent=2,ensure_ascii=False))
