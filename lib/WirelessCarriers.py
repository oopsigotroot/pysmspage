#!/usr/bin/env python
#WirelessCarriers.py
#
#Copyright 2012 - Patrick F. Wilbur <proj pdub net>
#
#


class WirelessCarrierEmailGateways:
    def __init__(self, path_to_wireless_carrier_flatfile=None):
        self.CarrierGateways = {'NONE': None}
        if path_to_wireless_carrier_flatfile == None or path_to_wireless_carrier_flatfile == '':
            self.CarrierGateways = {'NONE': None,
                'Boost Mobile': '@myboostmobile.com',
                'T-Mobile': '@tmomail.net',
                'Virgin Mobile': '@vmobl.com',
                'Cingular': '@cingularme.com',
                'Sprint Nextel': '@messaging.sprintpcs.com',
                'Verizon': '@vtext.com',
                'Nextel': '@messaging.nextel.com',
                'US Cellular': '@email.uscc.net',
                'SunCom': '@tms.suncom.com',
                'Powertel': '@ptel.net',
                'AT&T (Cingular)': '@txt.att.net',
                'Alltel': '@message.alltel.com',
                'Metro PCS': '@MyMetroPcs.com' }
        else:
            self.loadCarrierFlatfile(path_to_wireless_carrier_flatfile)

    def loadCarrierFlatfile(self, path):
        self.CarrierGateways = {'NONE': None}
        f = open(path)
        for line in f:
            name, emailSuffix = line.split(':')
            self.CarrierGateways[name] = emailSuffix.rstrip()
        f.close()
    def getCarrierGateways(self):
        return self.CarrierGateways

if __name__ == '__main__':
    print('')
    print('Creating test CarrierGateways from default constructor:')
    testCarrierMap = WirelessCarrierEmailGateways().getCarrierGateways()
    for k in testCarrierMap:
        print(' ', k)
        print('   ',testCarrierMap[k])

    print('')
    print('Writing test CarrierGateways flatfile...')
    fname = "test.fdb"
    fout = open(fname, "w")
    for k in testCarrierMap:
        if testCarrierMap[k] != None:
            fout.write(str(k) + ':' + str(testCarrierMap[k]) + "\n")
    fout.close()

    print('')
    print('Importing test CarrierGateways flatfile...')
    testCarrierMap = WirelessCarrierEmailGateways('test.fdb').getCarrierGateways()

    print('')
    print('CarrierGateways after flatfile import:')
    for k in testCarrierMap:
        print(' ', k)
        print('   ',testCarrierMap[k])

