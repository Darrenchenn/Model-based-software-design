#!/bin/bash
git clone https://github.com/Darrenchenn/Model-based-software-design.git
# Execute frontend_deploy.sh
echo "Executing frontend_deploy.sh..."
./frontend_deploy.sh

# Check the exit status of frontend_deploy.sh
if [ $? -eq 0 ]; then
    # If frontend_deploy.sh succeeded, execute deploy.sh
    echo "frontend_deploy.sh succeeded. Executing deploy.sh..."
    ./backend_deploy.sh
else
    # If frontend_deploy.sh failed, print an error message
    echo "Error: frontend_deploy.sh failed. Deployment aborted."
fi

