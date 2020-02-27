import jinja2
import yaml

def get_host_ip(network_addr):
  """
  network_addr = '10.100.22.28/30'
  output = ('10.100.22.29', '10.100.22.30')
  """
  last_octet = int(network_addr[:-3].split('.')[3])
  static = '.'.join(network_addr[:-3].split('.')[:3])
  #Verify network address is a valid /30
  if (last_octet-1)%3 != 0:
    return ()
  else:
    return (static+'.'+str(last_octet+1),static+'.'+str(last_octet+2))

template_file = 'template.j2'
var_file = 'vars.yml'
store_file = 'store.yml'

with open(var_file,'r') as f:
  vars = yaml.safe_load(f)

with open(store_file,'r') as f:
  stores = yaml.safe_load(f)

env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

for router in vars:
  conf_file = 'configs/'+router['hostname']+'.cfg'
  try:
    router_net_addr = stores['stores'][router['store']]
  except IndexError:
    print "Invalid store ID"
  else:
    (router['ip_addr'], router['neighbor']) = get_host_ip(router_net_addr)
    output = env.get_template(template_file).render(router)
    with open(conf_file,'w') as f:
      f.write(output)
