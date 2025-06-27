#!/bin/bash

# Caminho do ambiente virtual
VENV_PATH="/home/marco/projects/multi-agentes/amb10"

# Terminal para o receiver.py com ambiente virtual
gnome-terminal -- bash -c "echo 'Ativando ambiente e iniciando receiver.py'; source $VENV_PATH/bin/activate; python receiver.py; exec bash"

# Espera um pouco antes de iniciar o sender (opcional)
sleep 1

# Terminal para o sender.py com ambiente virtual
gnome-terminal -- bash -c "echo 'Ativando ambiente e iniciando sender.py'; source $VENV_PATH/bin/activate; python sender.py; exec bash"




