import app.wifimgr as wifimgr
import ujson
from app.ota_updater import OTAUpdater
from machine import Pin
from time import sleep
import network, gc, machine


def connectToWifiAndUpdate():
    print('Memory free', gc.mem_free())
    from app.ota_updater import OTAUpdater
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():

        print('connecting to network...')
        wifimgr.get_connection()

        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/4dragunov/tn_ota_snow', main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()

    if hasUpdated:
        machine.reset()
    else:
        del (otaUpdater)


wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


def startApp():
    import app.start


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")

connectToWifiAndUpdate()
startApp()








