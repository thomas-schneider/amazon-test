from cloudify_rest_client import CloudifyClient
from time import strftime as time
import os.path
import shutil
from time import sleep

activeClientIP = '172.25.1.29'
activeClient = CloudifyClient(activeClientIP)

passiveClientIP = '172.25.1.43'
passiveClient = CloudifyClient(passiveClientIP)


snapshot_id = time("%Y-%m-%d_%H:%M:%S")+'_host_'+activeClientIP


def add_entry_to_log_file(message, **kwargs):

        # add entry to log file
        with open('cloudify-snapshots.log', 'a+') as log_file:
                log_file.write(message)
        log_file.close()



def check_snapshot(snapshot_id, **kwargs): # Check if the snapshot was created without errors

        #List all snapshots
        snapshots_list = activeClient.snapshots.list()
        for snapshot in snapshots_list:
                if snapshot.get('id') == snapshot_id:
                        if snapshot.get('error') == '':
                                message = 'Snapshot {} successully created \n'.format(snapshot_id)
                                add_entry_to_log_file(message)
                        else:
                                message = 'Something went wrong while creating {}. The problem is: {} \n'.format(snapshot_id, snapshot.get('error'))
                                add_entry_to_log_file(message)

def create_snapshot(snapshot_id, **kwargs):
        activeClient.snapshots.create(snapshot_id=snapshot_id, include_metrics = False, \
        include_credentials = True)

def dl_snapshot(snapshot_id, **kwargs):
        sleep(10)
        #download created snapshot
        output_file = '/home/cloudify/cloudify-manager/{}.zip'.format(snapshot_id)
        print output_file
        activeClient.snapshots.download(snapshot_id=snapshot_id, output_file = output_file)
        sleep (5)
        #check if file was downloaded successfully or not and add an entry to the log file
        if os.path.isfile(output_file):
                message = 'Snapshot {} was successfully downloaded to {} \n'.format(snapshot_id,output_file)
        else:
                message = 'Something went wrong trying to download snapshot {} \n'. format(snapshot_id)

        add_entry_to_log_file(message)
        return output_file


def copy_snapshot(snapshot_id, saved_snapshot_file, **kwargs):
        if os.path.isfile(saved_snapshot_file):
                shutil.copy(saved_snapshot_file, '/tmp')
                message = 'Snapshot {} was successfully copied to /tmp folder \n'.format(snapshot_id)
        else:
                message = 'Something went wrong trying to save snapshot {} to /tmp folder \n'. format(snapshot_id)
        add_entry_to_log_file(message)


def delete_snapshot(snapshot_id, **kwargs):

        try:
                if (activeClient.snapshots.delete(snapshot_id=snapshot_id)):
                        message = 'Snapshot {} was successfully deleted \n'.format(snapshot_id)
                        add_entry_to_log_file(message)
        except Exception as e:
                message = str(e)
                add_entry_to_log_file(message)
                raise e


create_snapshot(snapshot_id)
check_snapshot(snapshot_id)
saved_snapshot_file = dl_snapshot(snapshot_id)
copy_snapshot(snapshot_id, saved_snapshot_file)