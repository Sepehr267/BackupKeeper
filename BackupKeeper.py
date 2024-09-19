#!/usr/bin/env python3
import os
import zipfile
import time
import random
import json
import argparse
from datetime import datetime
import subprocess
import sys

class Process:

    def __init__(self, process_file: str) -> None:
        self.process_file = process_file
        self.log_file = 'backup_log.txt' if not os.path.exists('backup_log.txt') else None

    def _process_id(self) -> int:
        return random.randint(100000, 999999)

    def create_process_data(self, pid: int, directory: str, backup_path: str, interval: int) -> bool:
        data = self.load_data()
        data[str(pid)] = {
            'directory': directory,
            'backup_path': backup_path,
            'interval': interval,
            'time_create_process': datetime.now().strftime('%Y%m%d_%H%M%S')
        }
        return self.write_data(data)

    def load_data(self) -> dict:
        try:
            with open(self.process_file, 'r', encoding='utf-8') as json_obj:
                data = json.load(json_obj)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def write_data(self, data: dict) -> bool:
        try:
            with open(self.process_file, 'w', encoding='utf-8') as json_obj:
                json.dump(data, json_obj, indent=4)
                return True
        except json.JSONDecodeError:
            return False

    def delete_process_data(self, pid: int) -> bool:
        data = self.load_data()
        pid_str = str(pid)
        if pid_str in data:
            del data[pid_str]
            return self.write_data(data)
        return False

    def get_files(self, directory: str, exclude_folder: str, backup_folder: str):
        file_paths = []
        is_full_path = os.path.isabs(exclude_folder)
        exclude_folder_name = os.path.basename(exclude_folder) if is_full_path else exclude_folder

        is_full_path_backup = os.path.isabs(backup_folder)
        backup_folder_name = os.path.basename(backup_folder) if is_full_path_backup else backup_folder

        for root, dirs, files in os.walk(directory):
            if is_full_path:
                if os.path.abspath(root) == os.path.abspath(exclude_folder) or os.path.abspath(root) == os.path.abspath(backup_folder):
                    continue
            else:
                if exclude_folder_name in dirs:
                    dirs.remove(exclude_folder_name)
                if backup_folder_name in dirs:
                    dirs.remove(backup_folder_name)

            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

    def cleanup_old_backups(self, backup_path: str, max_backups: int):
        backups = sorted([os.path.join(backup_path, f) for f in os.listdir(backup_path) if f.endswith('.zip')],
                        key=os.path.getmtime)
        print(f'\033[93mCleaning up old backups...\033[0m')
        print(f'\033[92mFound {len(backups)} backup files.\033[0m')
        while len(backups) > max_backups:
            old_backup = backups.pop(0)
            print(f'\033[91mRemoving old backup file: {old_backup}\033[0m')
            os.remove(old_backup)
        print(f'\033[92mCleanup complete. Remaining backups: {len(backups)}\033[0m')

    def backup(self, interval: int, directory: str, backup_path: str, exclude_folder: str, max_backups: int):
        os.makedirs(backup_path, exist_ok=True)
        pid = self._process_id()
        self.create_process_data(pid, directory, backup_path, interval)
        print(f'\033[94mProcess Auto-Backup Created For Folder: {directory} every {interval}s. Your PID for Kill Auto-Backup is {pid}.\033[0m')
        print(f'\033[93mFor Kill Use This Command : BackupKeeper -kill {pid}\033[0m')

        while True:
            timenow = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'{self.file_name}_{timenow}.zip'
            backup_file_path = os.path.join(backup_path, file_name)

            files = self.get_files(directory, exclude_folder, backup_path)

            with zipfile.ZipFile(backup_file_path, 'w') as zip_obj:
                for file in files:
                    zip_obj.write(file, os.path.relpath(file, directory))

            self.cleanup_old_backups(backup_path, max_backups)

            time.sleep(interval)

    def kill_process(self, pid: int):
        if self.delete_process_data(pid):
            print(f'\033[91mProcess with PID {pid} data has been removed from record.\033[0m')
            try:
                if os.name == 'nt':  # Windows
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
                else:  # Linux
                    subprocess.run(['kill', '-9', str(pid)], check=True)
                print(f'\033[91mProcess with PID {pid} has been terminated.\033[0m')
            except subprocess.CalledProcessError:
                print(f'\033[91mFailed to terminate process with PID {pid}.\033[0m')
        else:
            print(f'\033[91mProcess with PID {pid} not found in records.\033[0m')

    def list_active_processes(self):
        data = self.load_data()
        if data:
            print('\033[92mActive Backup Processes:\033[0m')
            for pid, info in data.items():
                print(f'PID: {pid} - Directory: {info["directory"]}, Backup Path: {info["backup_path"]}, Interval: {info["interval"]}s, Created At: {info["time_create_process"]}')
        else:
            print('\033[91mNo active backup processes found.\033[0m')

def main():
    parser = argparse.ArgumentParser(description='Run or manage backup scripts.')
    parser.add_argument('-time', type=int, help='Backup interval in seconds.')
    parser.add_argument('-directory', type=str, help='Directory to backup.')
    parser.add_argument('-exclude', type=str, default='', help='Folder to exclude from backup.')
    parser.add_argument('-bg', action='store_true', help='Run the process in the background.')
    parser.add_argument('-kill', type=int, help='PID of the process to kill.')
    parser.add_argument('-name', type=str, default='backup', help='Custom name for the backup files.')
    parser.add_argument('-dest', type=str, default='', help='Custom destination folder for backup files.')
    parser.add_argument('-log', action='store_true', help='Enable logging to a file.')
    parser.add_argument('-list', action='store_true', help='List active backup processes.')
    parser.add_argument('-max-backup', type=int, default=5, help='Maximum number of backup files to keep.')

    args = parser.parse_args()
    process = Process('process.json')
    process.file_name = args.name

    if args.kill is not None:
        process.kill_process(args.kill)
        return

    if args.list:
        process.list_active_processes()
        return

    if not args.time or not args.directory:
        parser.print_help()
        sys.exit(1)

    backup_interval = args.time
    backup_directory = args.directory
    exclude_folder = args.exclude
    backup_path = args.dest if args.dest else os.path.join(backup_directory, 'backup')
    max_backups = args.max_backup

    if args.bg:
        print("\033[92mRunning in background...\033[0m")
        pid = subprocess.Popen([sys.executable, __file__, '-time', str(backup_interval), '-directory', backup_directory, '-exclude', exclude_folder, '-max-backup', str(max_backups)],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True).pid
        print(f'\033[92mBackground process started with PID: {pid}\033[0m')
        print(f'\033[93mFor Kill Use This Command : BackupKeeper -kill {pid}\033[0m')
        process.create_process_data(pid, backup_directory, backup_path, backup_interval)
    else:
        process.backup(backup_interval, backup_directory, backup_path, exclude_folder, max_backups)

if __name__ == '__main__':
    main()
