#!/usr/bin/bash
# 
USER=$(id -un 1000)
DIR=$(dirname "$(readlink -f "$0")")
SERVICE_DIR=/home/${USER}/.local/share/kservices5/ServiceMenus
SERVICE="${DIR}/folderfromselected.desktop"

SCRIPT_DIR=/home/${USER}/.config/folderfromselected
SCRIPT="${DIR}/folderfromselected.py"
ICOS="${DIR}/icos"


if [[ ! -d ${SERVICE_DIR} ]]; then
    sudo -u ${USER} mkdir -p ${SERVICE_DIR}
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
    sudo -u ${USER} mkdir -p ${SCRIPT_DIR}
else
    if [[ -f ${SCRIPT} ]]; then
        if sudo -u ${USER} cp -f ${SCRIPT} ${SCRIPT_DIR}; then
            echo "folderfromselected.py, copiado com sucesso!"
        else
            echo "folderfromselected.py, erro ao copiar!"
        fi
        echo
        if sudo -u ${USER} cp -rf ${ICOS} ${SCRIPT_DIR}; then
            echo "Pastade icones copiada, copiado com sucesso!"
        else
            echo "Pastade icones, erro ao copiar!"
        fi
    fi
fi

exit