#!/bin/bash
docker_install() {
    echo -e "\033[1m 正在安装 docker... \033[0m "
    set -e
    set -x
    # install docker according to https://docs.docker.com/install/linux/docker-ce/centos/
    yum update -y
    yum install -y yum-utils device-mapper-persistent-data lvm2 -y
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum install docker-ce docker-ce-cli containerd.io -y
    systemctl start docker
    systemctl enable docker
    docker run hello-world
    # configure docker daemon according to https://kubernetes.io/docs/setup/production-environment/container-runtimes/
    cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
EOF
    systemctl daemon-reload
    systemctl restart docker
    set +e
    set +x
}

cri_install() {
    echo -e "\033[1m 正在安装 containerd作为CRI运行时... \033[0m "
    set -e
    set -x
    # install CRI-O according to https://kubernetes.io/docs/setup/production-environment/container-runtimes/#cri-o
    modprobe overlay
    modprobe br_netfilter
    cat > /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
    sysctl --system
    
    ##### never use CRI-O, it's piece of shit
    #yum-config-manager --add-repo=https://cbs.centos.org/repos/paas7-crio-311-candidate/x86_64/os/
    #yum install -y --nogpgcheck cri-o
    ###### fix cri-o installation bug according to https://github.com/cri-o/cri-o/issues/1767
    #ln -s /sbin/runc /usr/bin/runc
    #systemctl start crio
    #systemctl enable crio
    
    yum install -y containerd.io
    mkdir -p /etc/containerd
    containerd config default > /etc/containerd/config.toml
    systemctl restart containerd
    systemctl enable containerd
    set +e
    set +x
}

k8s_install() {
    echo -e "\033[1m 正在安装 kubernetes... \033[0m "
    set -e
    set -x
    # install kubelet according to https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl
    ##### in China, use aliyun k8s mirror instead
    cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kube*
EOF
    setenforce 0
    sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
    yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
    systemctl enable --now kubelet
    ##### turnoff swap and firewalld
    swapoff -a
    systemctl stop firewalld
    systemctl disable firewalld
    set +e
    set +x
}

k8s_master_create() {
    echo -e "\033[1m 正在使用kubeadm初始化集群... \033[0m "
    set -e
    set -x
    # master init
    echo -e "\033[1m     正在重置已存在的初始化\033[0m "
    kubeadm reset
    kubeadm config images pull
    echo -e "\033[1m     POD子网为10.244.X.X  主节点使用192.168.56.21网络接口\033[0m "
    kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.56.21
    # kubectl setting for root user
    mkdir -p /root/.kube
    cp -i /etc/kubernetes/admin.conf /root/.kube/config
    # using Calico as networking provider
    echo -e "\033[1m     使用Calico作为网络提供者 \033[0m "
    kubectl apply -f https://docs.projectcalico.org/v3.7/manifests/calico.yaml
    echo -e "\033[1m     配置集群主节点也可参与工作调度 \033[0m "
    kubectl taint nodes --all node-role.kubernetes.io/master-
    set +e
    set +x
}

dashboard_install() {
    echo -e "\033[1m     安装Dashboard \033[0m "
    set -e
    set -x
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended/kubernetes-dashboard.yaml
    cat <<EOF > /tmp/admin-role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
EOF
    kubectl apply -f /tmp/admin-role-binding.yaml
    token=$(kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}') | grep 'token:')
    grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> /tmp/kubecfg.crt
    grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> /tmp/kubecfg.key
    openssl pkcs12 -export -clcerts -inkey /tmp/kubecfg.key -in /tmp/kubecfg.crt -out kubecfg.p12 -name "kubernetes-client"
    rm -rf /tmp/kubecfg.crt
    rm -rf /tmp/kubecfg.key
    set +e
    set +x
    echo -e "\033[1m 请下载证书文件./kubecfg.p12并导入到你的浏览器\033[0m "
    echo -e "\033[1m 访问Dashboard：https://192.168.56.21:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/.\033[0m "
    echo -e "\033[1m 登录时请使用如下Token: \033[0m "
    echo '            '$token
}

dashboard_info() {
    echo 'https://192.168.56.21:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/.'
    token=$(kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}') | grep 'token:')
    echo $token
}

k8s_ctl4nonroot() {
    set -e
    set -x
    echo $1
    mkdir -p /home/${1}/.kube
    cp -i /etc/kubernetes/admin.conf /home/${1}/.kube/config
    chown ${1}:${1} /home/${1}/.kube/config
    set +e
    set +x
}

k8s_cluster_show() {
    echo -e "\033[1m node: \033[0m "
    kubectl get node
    echo -e "\n\033[1m pod: \033[0m "
    kubectl get pod
    echo -e "\n\033[1m pod network: \033[0m "
    kubectl get pods -n kube-system
}

k8s_joincmd() {
    token=$(kubeadm token list| awk '{print $1}' |sed -n '$p')
    if [ $(echo $token | wc -m) -lt 15 ];then
        echo "没有可用的Token，请创建新Token"
        exit -3
    fi
    cacert=$(openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //')
    echo kubeadm join 192.168.56.21:6443 --token $token --discovery-token-ca-cert-hash sha256:$cacert
}

if [ `id -u` -ne 0 ];then
	echo '请使用root用户执行'
    exit -1
fi

if [ $# -lt 2 ];then
    echo -e '使用方法：'
    echo -e '  k8s.sh install all\t\t\t依次安装docker,cri,k8s'
    echo -e '  k8s.sh install [docker|cri|k8s]\t指定安装某个组件。除非你了解这里的依赖关系，否则不要这样做'
    echo -e '  k8s.sh install dashboard\t\t安装Dashboard（集群创建完后再安装）'
    echo -e '  k8s.sh dashboard info\t\t显示Dashboard访问信息'
    echo -e '  k8s.sh kubectl [user name]\t\t使某用户可执行kubectl'
    echo -e '  k8s.sh cluster show\t\t展示集群信息'
    echo -e '  k8s.sh cluster create\t\t在主节点上创建集群'
    echo -e '  k8s.sh join showcmd\t\t要将新服务器加入集群，需要在那个服务器上执行的命令'
    echo -e '  k8s.sh join createtoken\t创建新token，24小时过期'
    echo -e '  k8s.sh join showtoken\t\t展示可用token'
    exit -2
fi

if [ "$1"x == "install"x ]; then
    if [ "$2"x == "all"x ]; then
        docker_install
        cri_install
        k8s_install
    elif [ "$2"x == "docker"x ]; then
        docker_install
    elif [ "$2"x == "cri"x ]; then
        cri_install
    elif [ "$2"x == "k8s"x ]; then
        k8s_install
    elif [ "$2"x == "dashboard"x ]; then
        dashboard_install
    fi
elif [ "$1"x == "dashboard"x ]; then
    if [ "$2"x == "info"x ]; then
        dashboard_info
    fi
elif [ "$1"x == "kubectl"x ]; then
    k8s_ctl4nonroot $2
elif [ "$1"x == "cluster"x ]; then
    if [ "$2"x == "show"x ]; then
        k8s_cluster_show
    elif [ "$2"x == "create"x ]; then
        k8s_master_create
    fi
elif [ "$1"x == "join"x ]; then
    if [ "$2"x == "showcmd"x ]; then
        k8s_joincmd
    elif [ "$2"x == "createtoken"x ]; then
        kubeadm token create
    elif [ "$2"x == "showtoken"x ]; then
        kubeadm token list
    fi
fi
