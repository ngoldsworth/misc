import datetime
import os
import time

# things
hostname = "google.com" # address to ping
interval = 10 # ~seconds between finishing one ping and starting next
log_prefix = "dads_exciting_ping_test" # log file name


param = '-n' if os.sys.platform.lower()=='win32' else '-c'
def ping_google(fileobj):
    t = datetime.datetime.now()
    response = os.system(f"ping {param} 1 {hostname}")
    success = response == 0

    res = 'up' if success else 'down'
    fileobj.write(f'{t.isoformat()}: {res}\n')
    return success


if __name__ == '__main__':

    # setup log
    st = datetime.datetime.now()
    timestamp = f'{st.year}-{st.month:>02}-{st.day:>02}-{st.hour:>02}{st.minute:>02}{st.second:>02}'
    log_file_name = f"{log_prefix}_{timestamp}.log"

    # open log file
    with open(log_file_name, 'w') as f:

        #ping forever
        while True:
            s = ping_google(f)
            time.sleep(interval)

