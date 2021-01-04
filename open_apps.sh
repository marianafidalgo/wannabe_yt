# chmod +x open_apps.sh
# ./open_apps.sh

gnome-terminal -- sh -c 'cd proxy; python3 proxy.py; exec bash'
gnome-terminal -- sh -c 'cd user_manager; python3 user.py; exec bash'
gnome-terminal -- sh -c 'cd videos; python3 videos_backup.py; exec bash'
gnome-terminal -- sh -c 'cd videos; python3 videos.py; exec bash'
gnome-terminal -- sh -c 'cd qa; python3 QA.py; exec bash'
gnome-terminal -- sh -c 'cd logs; python3 logs.py; exec bash'
