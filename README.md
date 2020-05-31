# lb2120

Command line access to the API for the Netgear LB2120 

## Usage

The LB2120 has its own web UI.  You'll need to know its IP address and the Admin password.  The IP defaults to 192.168.5.1, so only the Admin password is necessary to run.  By default, it will return the full JSON from the API, though optional parameters of "--object" and "--key" will allow you to pluck out exactly what you're interested in.

```
lb2120.py -p password -o failover -k wanConnected
```
This will return "True" if connected via wireline, and "False" if not

The also has the capability of sending text messages via the LB2120.  It's not the most lovely code in the world, but it works:

```
lb2120.py -p password -n phonenumber -t "text message"
