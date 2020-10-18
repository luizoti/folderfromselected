#!/usr/bin/bash
# 
if [[ ! -f $(which python3) ]]; then
    echo 
    echo "_____________ Instalando Python3 _____________"
    sudo apt-get update -y 
    sudo apt-get install python3 -y
fi

GETPIP=/tmp/get-pip.py
        
if [[ ! -f ${GETPIP} ]]; then
    echo 
    echo "_____________ Instalando PIP _____________"
    curl https://bootstrap.pypa.io/get-pip.py -o ${GETPIP}
fi

if sudo python3 ${GETPIP}; then
    echo "Sucesso ao instalar PIP"
else
    echo "Erro ao instalar PIP"
fi

echo 
echo "_____________ Instalando pyqt5 _____________"
if sudo pip3 install pyqt5; then
    echo "Sucesso ao instalar pyqt5"
else
    echo "Erro ao instalar pyqt5"
fi

USER=$(id -un 1000)
DIR=$(dirname "$(readlink -f "$0")")
SERVICE_DIR=/home/${USER}/.local/share/kservices5/ServiceMenus
SERVICE="${DIR}/folderfromselected.desktop"

SCRIPT_DIR=/home/${USER}/.config/folderfromselected

icoold="Icon=.*"
iconew="Icon=${DIR}/icos/folder.png"

function install(){
    if [[ ! -d ${SERVICE_DIR} ]]; then
        sudo mkdir -p ${SERVICE_DIR}
    fi

    if sed -i "s|$icoold|$iconew|g" "${DIR}/folderfromselected.desktop"; then
        if [[ -f ${SERVICE} ]]; then
            if sudo cp -f ${SERVICE} ${SERVICE_DIR}; then
                echo "folderfromselected.desktop, copiado com sucesso!"
            else
                echo "folderfromselected.desktop, erro ao copiar!"
            fi
        fi
    fi

    echo
    if [[ ! -d ${SCRIPT_DIR} ]]; then
        echo
        echo "_____________ Baixando folderfromselected _____________"
        sudo -u ${USER} git clone 'https://github.com/luizoti/folderfromselected.git' ${SCRIPT_DIR}
    else
        echo
        echo "_____________ Atualizando folderfromselected _____________"
        cd ${SCRIPT_DIR}
        sudo -u ${USER} git pull origin master
    fi
}

install

exit