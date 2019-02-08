## This is server deploy documentation

Server deploy performed by Anisble. **Ansible** is configuration management, and application deployment tool. 

Running **development** of the project:

Dev server created by Vagrant. **Vagrant** is product for building and maintaining portable virtual software development environments.

For creating local ubuntu server run:

```
vagrant up
```

For provisioning server with necessary configuration run:
```
ansible-playbook -i inventory.ini.txt playbook.yml -l dev
```



Running **production** of the project:

Add host and access data to inventory.ini.txt file. For Example:
```
[dev]
...

[prod]
aws ansible_host=ec2-xx-xx-xxx-xx.us-west-2.compute.amazonaws.com ansible_user=USER ansible_port=22 ansible_ssh_private_key_file=~/SECRET.pem

```
For provisioning server with necessary configuration run:
```
ansible-playbook -i inventory.ini playbook.yml -l prod
```