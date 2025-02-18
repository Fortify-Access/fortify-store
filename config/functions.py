import subprocess
from django.conf import settings
from django.template.loader import render_to_string

from inbounds import models

def reload_singbox():
    try:
        subprocess.check_output([settings.SING_BOX_PATH, "run"])
        return True
    except Exception as e:
        print(e)
        return False

def reload_nginx():
    nginx_config = render_to_string('services/user_paths_template.conf', {'users': models.InboundUser.objects.all()})
    with open('services/user_paths.conf', 'w') as config:
        config.write(nginx_config)
    
    subprocess.run(['nginx', '-s', 'reload'])
