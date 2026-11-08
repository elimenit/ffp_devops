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
    
    if [[ ! -d "$dir/.venv" ]]; then
        python3 -m venv .venv
    fi

    source .venv/bin/activate && pip install -r requirements.txt --retries=30 1>/dev/null
}

init_app() {
    dir=$1
    cd $dir
    uvicorn main:app --reload  --port 10000 --host 0.0.0.0
}

main() {
    dir_backend="$DIR_WORK/backend"

    init_virtual_enviroment $dir_backend
    init_app $dir_backend

}

main
