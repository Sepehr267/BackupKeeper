# BackupKeeper 🔒📄

BackupKeeper is a script designed to manage and automate backups of specified directories. It supports scheduling backups, excluding certain folders, and maintaining a defined number of backup files. This tool is compatible with both Windows and Linux systems.

## Features ✨

- **Automated Backups** ⏳: Schedule backups at defined intervals.
- **Exclusions** 🚫: Exclude specific folders from backups.
- **Process Management** 🔄: Start, kill, and list active backup processes.
- **Backup Cleanup** 🗑️: Maintain a maximum number of backup files by automatically removing older ones.
- **Run in the Background** 🌙: Backup is performed normally and in the background.

## Installation 🛠️

### Linux Setup Instructions 🐧

1. **Download BackupKeeper**
    ```bsah
    git clone https://github.com/Sepehr267/BackupKeeper
    cd BackupKeeper
    ```
2. **Move the Script to a System Directory**:
    ```bash
    sudo mv BackupKeeper.py /usr/local/bin/BackupKeeper
    ```

3. **Make the Script Executable**:
    ```bash
    sudo chmod +x /usr/local/bin/BackupKeeper
    ```

4. **Update Your PATH**:
    ```bash
    echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
    source ~/.bashrc
    ```

### Windows Setup Instructions 🏁

#### 1. **Download BackupKeeper**

- Download the BackupKeeper zip file.
- Unzip the file and place its contents in a fixed location, such as:

  `C:\BackupKeeper`

- Ensure the `BackupKeeper.py` file is located at:

  `C:\BackupKeeper\BackupKeeper.py`

- **Next**, create a new file named `BackupKeeper.bat` in the same folder as `BackupKeeper.py`.

- **Open** the `BackupKeeper.bat` file with a text editor (like Notepad) and **copy and paste** the following code into it:

  ```batch
  @echo off
  python C:\BackupKeeper\BackupKeeper.py %*
  ```
- Make sure to replace `C:\BackupKeeper\BackupKeeper.py` with the actual file path where you saved `BackupKeeper.py`
#### 2. **Add the Directory to PATH**

##### For Windows 10/11:

1. Open the Start Menu and search for **"Environment Variables."**
2. Select **"Edit the system environment variables."**
3. In the **System Properties** window, click the **"Environment Variables"** button.
4. In the **Environment Variables** window, find and select the **"Path"** variable under **"System variables."**
5. Click **"Edit"** and then **"New."**
6. Add the directory path where your `BackupKeeper.py` file is located (e.g., `C:\BackupKeeper`).
7. Click **"OK"** to close all dialog boxes.

##### For Windows 7/8:

1. Right-click on **"Computer"** and select **"Properties."**
2. Click **"Advanced system settings."**
3. In the **System Properties** window, click the **"Environment Variables"** button.
4. Find the **"Path"** variable under **"System variables"** and select it.
5. Click **"Edit"** and add the directory path to the end of the existing path, separated by a semicolon (e.g., `C:\BackupKeeper;`).
6. Click **"OK"** to close all dialog boxes.

### Or you can put the `BackupKeeper.py` file next to your project folder and use it. 📂

## Usage 📝

Now, just open the terminal and type the BackupKeeper command to display the menu.

```bash
sepehr@DESKTOP-BSTUMQD:~$ BackupKeeper
usage: BackupKeeper [-h] [-time TIME] [-directory DIRECTORY] [-exclude EXCLUDE] [-bg] [-kill KILL] [-name NAME] [-dest DEST]
                    [-log] [-list] [-max-backup MAX_BACKUP]

Run or manage backup scripts.

options:
  -h, --help            show this help message and exit
  -time TIME            Backup interval in seconds.
  -directory DIRECTORY  Directory to backup.
  -exclude EXCLUDE      Folder to exclude from backup.
  -bg                   Run the process in the background.
  -kill KILL            PID of the process to kill.
  -name NAME            Custom name for the backup files.
  -dest DEST            Custom destination folder for backup files.
  -log                  Enable logging to a file.
  -list                 List active backup processes.
  -max-backup MAX_BACKUP
                        Maximum number of backup files to keep.
sepehr@DESKTOP-BSTUMQD:~$
```

For example, to backup the Project folder, this command prepares a backup of the `/home/sepehr/Project` directory every 60 seconds and places it in the `/home/sepehr/Project/backup folder`. The `-bg` flag is for the backup process to be in the background:

```bash
sepehr@DESKTOP-BSTUMQD:~/Project$ BackupKeeper -directory /home/sepehr/Project -time 60 -bg
Running in background...
Background process started with PID: 245
For Kill Use This Command : BackupKeeper -kill 245
sepehr@DESKTOP-BSTUMQD:~/Project$ 
```
Now we can turn off the backup with the `-kill` flag
```bash
sepehr@DESKTOP-BSTUMQD:~/Project$ BackupKeeper -kill 245
Process with PID 245 data has been removed from record.
Process with PID 245 has been terminated.
```
<br><br>
# Notes 📝
By default, after 5 zip files are created in the backup folder, BackupKeeper replaces the new backup files in order from oldest to newest.

To avoid replacement, add the `-max-backup` parameter along with the number of backup files to the command:
```bash
BackupKeeper -directory /home/sepehr/Project -time 60 -max-backup 10 -bg
```
<br><br>
**Author:** Sepehr0Day  
**Version:** 1.0.0<br>
**Telegram:** [t.me/Sepehr0Day](https://t.me/Sepehr0Day)  
**Telegram Channel:** [t.me/DevSepehr](https://t.me/DevSepehr)  

*If you found BackupKeeper helpful and want to support its development, please consider giving the repository a star! ⭐*