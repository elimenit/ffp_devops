#!/bin/bash
# Setup for Frontend Web Development

DIR_WORK="$HOME/Proyectos/ffp_devops"

download_resources() {
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3-venv python3-pip uvicorn
}

init_virtual_enviroment() {
    dir=$1 
    cd $dir
    echo $dir
    if [[ ! -d "$dir/.venv" ]]; then
        python3 -m venv .venv
    fi

    source .venv/bin/activate && pip install -r requirements.txt --retries=30 1>/dev/null
}

init_app() {
    dir=$1
    cd $dir
    uvicorn app:app --reload --port 15000 # --host 0.0.0.0
}

main() {

    dir_frontend="$DIR_WORK/frontend"
    init_virtual_enviroment $dir_frontend
    init_app $dir_frontend
}

main
