# automated_messages_via_domain
 send automated emails

## Problem...
We receive Askari Bank E-Statements in our gmail account and all the PDFs are maintained at google space. Gmail system is so fast that we can search any entry in 1000s of pdfs and gmail pulls up the file that cotains that entry in milli seconds.

In November 2022 Askari Bank made there statements password protected due to security reasons and gmail is unable to search entries in a password protected pdf. So....

## Solution
I set a forwarder to my gmail account that all email I received that contains "Encrypted, Encrypt or Password" and contains an attachment will be automatically forwarded to my domain email address where those email's attachments will be downloaded and then I provide it a file with passwords. It will download all the pdfs and then try to decrypt them by inserting passwords provided in the list and if the password found it makes a un-encrypted copy of the file and remove the password protected one. Once all the attachments are unlocked will be return to the address from where the domain email address recieved them. If the attachment is not password protected the application after receiving the email will do nothing.
