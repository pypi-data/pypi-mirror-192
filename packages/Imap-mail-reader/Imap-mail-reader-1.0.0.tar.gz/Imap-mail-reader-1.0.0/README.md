# Imap-mail-reader
The aim of this project is to simplify python mail reading from imap

## Install
PIP incoming soon

## Usage

### Mail Reader class methods and attributes
`from ImapMailManager import MailReader` to import the reader

`reader = MailReader(Imap-server address, Usename, Token)` to instantiate the reader

`reader.Connect()` to connect to the imap server using credentials

`reader.getUnreadMails()` to connect to the imap server using credentials

`reader.messages` is a variable containing a list of message class

### Message class contains following attributes : 
`msgFrom` : string
`to` : string
`date` : string 
`attachments` : list of File 
`subject` : string 
`body` : string 
`htmlBody` : string 

### File class contains following attributes : 
`name` : string
`content` : string

Example of usage in test.py
