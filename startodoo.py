#!/usr/local/bin/python3.10

import sys
import subprocess
import re

docker_containers = {
    'db14': 'acaae37fb763',
    'db15': '5e539dcce5bf'
}

help_msg = """
Simple odoo script

startodoo <version>/<op_params>

Optional parameters:

--help

"""



class start_odoo:
    def __init__(self, version:int):
        self.version = version
        if self.version >= 15:
            self.python_version = '3.10'
        elif self.version < 15:
            self.python_version = '3.8'

    def start_odoo_server(self, version, python_version):
        start_odoo = subprocess.run(f'/opt/odoo{version}/venv-odoo{version}/bin/python{python_version} /opt/odoo{version}/odoo-bin -c /etc/odoo{version}.conf', stdout=subprocess.PIPE, shell=True)




    def start_docker_db(self):
        p1 = subprocess.run(['docker', 'ps'], stdout=subprocess.PIPE, text=True)

        StdOut = p1.stdout
        is_db_present = lambda x: docker_containers.get(f"db{x}")
        if is_db_present(self.version):
            x = re.search(docker_containers.get(f"db{self.version}"), StdOut)
            if x:
                print(f"DATABASE db{self.version} is ONLINE!\n")
                print(f"Starting odoo server...\n")
                self.start_odoo_server(self.version, self.python_version)


            else:
                print(f"DATABASE db{self.version} is NOT RUNNING!\n Starting database {self.version}...\n\n")
                start_db_p = subprocess.run(f'docker start db{self.version}', stdout=subprocess.PIPE, shell=True)
                if start_db_p.stdout:
                    print(f"DB server (db{self.version}) has started successfully!\n")
                    print(f"Starting odoo server...\n")
                    self.start_odoo_server(self.version, self.python_version)
                else:
                    print(f"Something went WRONG: DB server (db{self.version}) started with exit status 1\n")

        else:
            raise TypeError(f"There is not a db registered with that version ({self.version})\n")
        # if item == docker_containers.get(f'db{self.version}'):
        #     print(f"{item} is ONLINE\n\n")
        # else:
       
        


#     for line in data_file.readlines():
# ...             data = line.split()
# ...             print(data)

try:
    if sys.argv[1] == '--help':
        print(help_msg)
    else:

        initialize = start_odoo(int(sys.argv[1]))
        initialize.start_docker_db()

except IndexError:
    print("[INDEX ERROR] you need to add a DB version\n")
    print(help_msg)

except KeyboardInterrupt:
    quit()










