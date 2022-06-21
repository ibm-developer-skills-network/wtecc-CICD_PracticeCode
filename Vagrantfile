# -*- mode: ruby -*-
# vi: set ft=ruby :

######################################################################
# DevOps Workshop MicroK8s Environment
######################################################################
Vagrant.configure("2") do |config|
  config.vm.define "workshop" do |workshop|
    workshop.vm.box = "bento/ubuntu-21.04"
    workshop.vm.hostname = "workshop"

    # Set up networking
    workshop.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
    # workshop.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
    # workshop.vm.network "forwarded_port", guest: 10443, host: 10443, host_ip: "127.0.0.1"
    
    workshop.vm.network "private_network", ip: "192.168.33.10"

    ############################################################
    # Configure Vagrant to use VirtualBox:
    ############################################################
    workshop.vm.provider "virtualbox" do |vb|
      # vb.name = "workshop"
      vb.memory = 1024
      vb.cpus = 2
    end

    ############################################################
    # Provider for Docker on Intel or ARM (aarch64)
    ############################################################
    config.vm.provider :docker do |docker, override|
      override.vm.box = nil
      docker.image = "rofrano/vagrant-provider:ubuntu"
      docker.remains_running = true
      docker.has_ssh = true
      docker.privileged = true
      docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:ro"]
      # Uncomment to force arm64 for testing images on Intel
      # docker.create_args = ["--platform=linux/arm64"]     
    end    

    ############################################################
    # Copy some host files to configure VM like the host
    ############################################################

    # Copy your .gitconfig file so that your git credentials are correct
    if File.exists?(File.expand_path("~/.gitconfig"))
      workshop.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
    end

    # Copy your ssh keys for github so that your git credentials work
    if File.exists?(File.expand_path("~/.ssh/id_rsa"))
      workshop.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
    end

    # Copy your .vimrc file so that your VI editor looks nice
    if File.exists?(File.expand_path("~/.vimrc"))
      workshop.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
    end

    ############################################################
    # Create a Python 3 environment for development work
    ############################################################
    workshop.vm.provision "shell", inline: <<-SHELL
      echo "****************************************"
      echo " INSTALLING PYTHON 3 ENVIRONMENT..."
      echo "****************************************"
      # Install Python 3 and dev tools 
      apt-get update
      apt-get install -y git vim tree wget jq build-essential python3-dev python3-pip python3-venv apt-transport-https
      apt-get upgrade python3

      # Create a Python3 Virtual Environment and Activate it in .profile
      sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
      sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
      sudo -H -u vagrant sh -c '. ~/venv/bin/activate && pip install -U pip && pip install wheel'
      sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'

      # Check versions to prove that everything is installed
      python3 --version

      # Install Visual Studio Code server
      # curl -fsSL https://code-server.dev/install.sh | sh
      # sudo systemctl enable --now code-server@vagrant
    SHELL

    ############################################################
    # Provision Docker with Vagrant before installing Kubernetes
    ############################################################
    workshop.vm.provision :docker do |d|
      d.pull_images "python:3.8-slim"
      d.pull_images "redis:6-alpine"
      d.run "redis:6-alpine",
        args: "-d --name redis -p 6379:6379 -v redis:/data"
    end

    # ############################################################
    # # Create a Kubernetes Cluster
    # ############################################################
    # workshop.vm.provision "shell", inline: <<-SHELL
    #   # snap install kubectl --classic
    #   snap install microk8s --classic
    #   microk8s.status --wait-ready
    #   microk8s.enable dns
    #   microk8s.enable dashboard
    #   microk8s.enable registry
    #   # microk8s.kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml
    #   microk8s.enable ingress
    #   snap alias microk8s.kubectl kubectl
    #   usermod -a -G microk8s vagrant
    #   echo "alias mk='/snap/bin/microk8s'" >> /home/vagrant/.bash_aliases
    #   echo "alias kc='/snap/bin/kubectl'" >> /home/vagrant/.bash_aliases
    #   chown vagrant:vagrant /home/vagrant/.bash_aliases
    #   sudo -H -u vagrant sh -c 'mkdir ~/.kube && microk8s.kubectl config view --raw > ~/.kube/config'
    #   kubectl version --short  

    #   # Install Helm
    #   # snap install helm --classic
    #   # helm version
    #   # helm repo add stable https://kubernetes-charts.storage.googleapis.com/
    #   # helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com
    #   # helm repo add bitnami https://charts.bitnami.com/bitnami
    #   # helm repo update
      
    #   microk8s.config > /home/vagrant/.kube/config
    #   chown vagrant:vagrant /home/vagrant/.kube/config
    #   chmod 600 /home/vagrant/.kube/config
    # SHELL

  end
end
