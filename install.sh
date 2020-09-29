#!/usr/bin/bash
# 
USER=$(id -un 1000)
DIR=$(dirname "$(readlink -f "$0")")
SERVICE_DIR=/home/${USER}/.local/share/kservices5/ServiceMenus
SERVICE="${DIR}/folderfromselected.desktop"

SCRIPT_DIR=/home/${USER}/.config/folderfromselected
SCRIPT="${DIR}/folderfromselected.py"
ICOS="${DIR}/icos"


function install(){
    if [[ ! -d ${SERVICE_DIR} ]]; then
        sudo mkdir -p ${SERVICE_DIR}
    else
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
        sudo -u ${USER} git clone 'https://github.com/luizoti/folderfromselected.git' ${SCRIPT_DIR}
    else
        cd ${SCRIPT_DIR}
        sudo -u ${USER} git pull origin master
    fi
}

if [[ -f "/usr/bin/plasma_session" ]] && [[ ${DESKTOP_SESSION} == "plasma" ]]; then
    install
else
    echo "Esse escript foi escrito para o KDE, caso esteja usando outro Desktop Enviroment, instale manualmente."
fi

exit