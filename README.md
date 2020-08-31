# PS2

To run the bot:

roslaunch m2wr_description spawn.launch

To run any code:

rorun m2wr_description [python_file_name]

For 2 bots

rosrun m2wr_description try.launch

lane detection : https://colab.research.google.com/drive/1a4C4MPtyXVWUm15BKHll8B_8dPn7aquV

Rotate bots:

main: rosrun m2wr_description rotate_main.py

follow: rosrun m2wr_description rotate_follower.py

Just to run main bot, type:
rostopic pub /cmd_vel (Just now press TAB keys)


