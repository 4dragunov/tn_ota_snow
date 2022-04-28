
from machine import ADC, Pin
import time, utime
import machine
import urequests

import network

import ujson
import app.secrets as secrets

file = open('config.json')
config_datas = ujson.load(file)

uId1 = config_datas['sensor1']['id']
url = secrets.URL

uId2 = config_datas['sensor2']['id']


adc1 = ADC(Pin(39))
adc1.atten(ADC.ATTN_11DB)
imp1 = Pin(26, Pin.OUT)
imp1.off()
rev1 = Pin(0, Pin.OUT)
rev1.off()

adc2 = ADC(Pin(36))
adc2.atten(ADC.ATTN_11DB)
imp2 = Pin(25, Pin.OUT)
imp2.off()
rev2 = Pin(4, Pin.OUT)
rev2.off()

def average(data_list):
    try:
        for i in range(len(data_list) - 1):
            for j in range(len(data_list) - i - 1):
                if data_list[j] > data_list[j + 1]:
                    data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]

        result = []
        med = len(data_list) // 2
        zero_delta = abs(data_list[med] - data_list[med + 1])
        for i in range(med, len(data_list) - 1):
            if data_list[i + 1] - data_list[i] <= zero_delta:
                result.append(data_list[i])

        for i in range(1, med):
            if data_list[i] - data_list[i - 1] <= zero_delta:
                result.append(data_list[i])
        if sum(result) != 0:
            avg_result = sum(result) / len(result)
        else:
            avg_result = 0
        print('average result is ', avg_result)
        return avg_result
    except:
        return data_list[0]


def sendData(data, sensor_uId):
    response_data = urequests.post(url, json={"value": data, "sensor": sensor_uId})
    if response_data.status_code != 201:
        print(response_data.status_code)
        machine.reset()


def measure(adc, imp, rev):
    dataList = []

    imp.on()
    time.sleep(0.1)
    for _ in range(50):
        dataList.append(adc.read_u16())
        time.sleep(0.1)

    val = average(dataList)
    imp.off()
    time.sleep(0.5)
    reverse(rev)
    print('measure result is ', val)
    return round(val, 0)


def reverse(rev):
    rev.on()
    time.sleep(0.2)
    rev.off()
    time.sleep(0.5)


def connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config_datas['wifi']['ssid'], config_datas['wifi']['password'])
    while not sta_if.isconnected():
        pass
    print('OK - network config:', sta_if.ifconfig())


def main():
    import gc
    while True:
        try:
            print('main for i in range 100')
            for i in range(1000):
                #print('main measure ', i)
                time.sleep(1)
                data1 = measure(adc1, imp1, rev1)
                #print('main measure OK', i)
                #print('main send data ', i, data)
                time.sleep(1)
                sendData(data1, uId1)
                print('data1 send complete ', i, data1)
                data2 = measure(adc2, imp2, rev2)
                sendData(data2, uId2)
                print('data2 send complete ', i, data2)
                time.sleep(4)
                gc.collect()
            machine.reset()

        except:
            print('main error')
            time.sleep(1)
            machine.reset()


main()


