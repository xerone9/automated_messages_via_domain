# automated_messages_via_domain
 send automated emails

## Problem...
We receive Askari Bank E-Statements in our gmail account and all the PDFs are maintained at google space. Gmail system is so fast that we can search any entry in 1000s of pdfs and gmail pulls up the file that cotains that entry in milli seconds.

In November 2022 Askari Bank made there statements password protected due to security reasons and gmail is unable to search entries in a password protected pdf. So....

## Solution
I set a forwarder to my gmail account that all email I received that contains "Encrypted, Encrypt or Password" word and contains an attachment will be automatically forwarded to my domain email address where those email's attachments will be downloaded. It will download all the pdfs and then try to decrypt them by inserting passwords provided in the list and if the password found it makes a un-encrypted copy of the file and remove the password protected one. Once all the attachments are unlocked will be return to the address from where the domain email address recieved them. If the attachment is not password protected the application after receiving the email will do nothing.

A cron job has been set that triggers that applcation every 3rd hour cant run all the time as my domain server CPU usage will be at its peak all the time

## Changelog 1.1

1- Added statement summary. Now decrypted pdf statement will be send back with account summary

2- Signature and social links added

3- When all statements are send back. Another email will be sent to will alla account names and Available balances
