import os
def get_file(api_key):
    out = ""
    out += """
    #!/bin/bash

    # create spinup user
    adduser spinup --disabled-password --quiet;

    mkdir /home/spinup/spinup

    # become spinup
    su spinup;
    """
    for filename in os.listdir("../daemon"):
        if filename.endswith(".py") or filename == "requirements.txt":
            out += "echo '"
            out += open("../daemon/" + filename).read().replace("'", "\\'")
            out += "' > /home/spinup/spinup/" + filename + ";"

    out += "echo 'api_key = \"" + api_key + "\"' > /home/spinup/spinup/secret.py;"


    out += "yes | apt-get install python-dev;"
    out += "pip install -r /home/spinup/spinup/requirements.txt;"
            

    out += """
    # Generate init.d file
    echo '
    #!/bin/bash
    # SpinUp daemon

    DAEMON_PATH="/home/spinup/spinup"

    DAEMON="python daemon.py"
    DAEMONOPTS=""

    NAME=spinup
    DESC="SpinUp daemon"
    PIDFILE=/var/run/$NAME.pid
    SCRIPTNAME=/etc/init.d/$NAME

    case "$1" in
    start)
            printf "%-50s" "Starting $NAME..."
            cd $DAEMON_PATH
            PID=`$DAEMON $DAEMONOPTS > /dev/null 2>&1 & echo $!`
            #echo "Saving PID" $PID " to " $PIDFILE
            if [ -z $PID ]; then
                printf "%s\n" "Fail"
            else
                echo $PID > $PIDFILE
                printf "%s\n" "Ok"
            fi
    ;;
    status)
            printf "%-50s" "Checking $NAME..."
            if [ -f $PIDFILE ]; then
                PID=`cat $PIDFILE`
                if [ -z "`ps axf | grep ${PID} | grep -v grep`" ]; then
                    printf "%s\n" "Process dead but pidfile exists"
                else
                    echo "Running"
                fi
            else
                printf "%s\n" "Service not running"
            fi
    ;;
    stop)
            printf "%-50s" "Stopping $NAME"
                PID=`cat $PIDFILE`
                cd $DAEMON_PATH
            if [ -f $PIDFILE ]; then
                kill -HUP $PID
                printf "%s\n" "Ok"
                rm -f $PIDFILE
            else
                printf "%s\n" "pidfile not found"
            fi
    ;;
    restart)
            $0 stop
            $0 start
    ;;
    *)
            echo "Usage: $0 {status|start|stop|restart}"
            exit 1
    esac
    ' > /etc/init.d/spinup
    chmod +x /etc/init.d/spinup
    update-rc.d spinup start 2 1 . stop 0 1 .
    """
    return out

if __name__ == '__main__':
    print get_file("MY_API_KEY")
