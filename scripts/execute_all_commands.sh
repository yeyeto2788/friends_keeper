#!/bin/bash
COMMAND="poetry run friends_keeper"



printf "\n\n*******************************"
printf "\nRemoving database and logs\n"
printf "*******************************"
rm ./friends_keeper.db ./friends_keeper.log


printf "\n\n**********************"
printf "\nCreating test data\n"
printf "**********************"
.venv/bin/python ./scripts/create_test_data.py

printf "\n\n***************************************"
printf "\nShow initial friends (should be 10)\n"
printf "***************************************"
eval $COMMAND show friends

printf "\n\n*******************************************"
printf "\nAdd a new friend which should get ID 11\n"
printf "*******************************************"
eval $COMMAND add friend --nickname testnickname11

printf "\n\n***********************************************"
printf "\nShow all friends including recently created\n"
printf "***********************************************"

eval $COMMAND show friends

printf "\n\n*****************************************"
printf "\nShow all notifications (should be 11)\n"
printf "*****************************************"
eval $COMMAND show notifications

printf "\n\n*************************************"
printf "\nDelete notification for friend 10\n"
printf "*************************************"
eval $COMMAND delete notification --friend-id 10

printf "\n\n*****************************************"
printf "\nShow all notifications (should be 10)\n"
printf "*****************************************"
eval $COMMAND show notifications

printf "\n\n**********************************"
printf "\nAdd notification for friend 10\n"
printf "**********************************"
eval $COMMAND add notification --friend-id 10

printf "\n\n************************************"
printf "\nDelete notification for friend 3\n"
printf "************************************"
eval $COMMAND delete notification --id 3

printf "\n\n*****************************************"
printf "\nShow all notifications (should be 10)\n"
printf "*****************************************"
eval $COMMAND show notifications


printf "\n\n*******************"
printf "\nDelete friend 3\n"
printf "*******************"
eval $COMMAND delete friend --id 3


printf "\n\n*******************************"
printf "\nShow all friends (Should be 10)\n"
printf "***********************************"
eval $COMMAND show friends --show-inactive true


printf "\n\n***********************"
printf "\nShow configuration used\n"
printf "\n\n***********************"
eval $COMMAND show configuration


printf "\n\n************************************"
printf "\nUpdate notification event for friend 5\n"
printf "****************************************"
eval $COMMAND update notification --friend-id 5 --date $(date +%d/%m/%y)


printf "\n\n*****************"
printf "\nExecute main core\n"
printf "*********************"
eval $COMMAND run