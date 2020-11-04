import os

'''
ceragon.txt
uf_id site_id shortname tagging(tag/access) service(LLI, LL, PBX...) vlan(vlan-ok szóközzel elválasztva)

'''

def open_ceragon_txt():
    #ceragon.txt fájl megnyitása, tartalmának kiolvasása
    with(open('C:\\Temp\\ceragon.txt','r')) as ceragon_txt:
        return (ceragon_txt.readlines())


def data_grabber(sor_szama):
    #ceragon.txt fájl adott sorának feldolgozása
    ceragon_txt = open_ceragon_txt()
    datas = ceragon_txt[sor_szama].split()
    uf_id = datas[0]
    site_id = datas[1]
    shortname = datas[2]
    tagging = datas[3]
    service = datas[4]
    vlan = datas[5::]
    #for i in range(0,len(datas)-4):
    #    vlan.append(datas[i+4])
    return uf_id, site_id, shortname, tagging, service, vlan

def write_common_lines(mydatas, oldal):
    #létrehozza a fájlt, és bemásolja azokat a sorokat, amikben nincsenek változók
    if mydatas[3] ==  'tag':
        servicetype = '_Bundle_C_'
    elif mydatas[3] == 'access':
        servicetype = '_c_vlan_'
    else:
        exit()
    with(open('C:\\Temp\\' + mydatas[0] + '\\' + mydatas[0] + servicetype + oldal + '.txt', 'w')) as bundlec:               #'C:\\Temp\\' + mydatas[0] + '\\' folderben hozza létre a fájlokat
        bundlec.write('platform management ntp set admin enable ntp-version ntpv4 ntp-server-ip-address-1 192.168.45.236\n')
        bundlec.write('ethernet service sid 1\n')
        bundlec.write('sp delete spid 1\n')
        bundlec.write('sp delete spid 2\n')
        bundlec.write('exit\n')
        bundlec.write('platform security protocols-control snmp version set v2\n')
        bundlec.write('platform if-manager set interface-type ethernet slot 1 port 2 admin down\n')
        bundlec.write('platform if-manager set interface-type ethernet slot 1 port 3 admin down\n')



def append_data(mydatas, oldal):
    #megynyitja a fájlt, és hozzáfűzi a változókat tartalmazó sorokat
    if oldal == 'belso':
        unit_name = '0' + mydatas[1] + '_CER_' + mydatas[2] + '\n'
    elif oldal == 'ugyfel':
        unit_name = mydatas[0] + '_CER_' + mydatas[2] + '\n'
    if mydatas[3] ==  'tag':
        servicetype = '_Bundle_C_'
        service_name = mydatas[0] + '_' + mydatas[2]
        service_desc = service_name
    elif mydatas[3] == 'access':
        servicetype = '_c_vlan_'
        service_name = mydatas[0] + '_s1_' + mydatas[4]
        service_desc = mydatas[0] + '_' + mydatas[2] + '_s1_' + mydatas[4]
    else:
        exit()
    vlan = mydatas[5]
    with(open('C:\\Temp\\' + mydatas[0] + '\\' + mydatas[0] + servicetype + oldal + '.txt','a')) as bundlec:
        bundlec.write('platform management system-name set name ' + unit_name)
        bundlec.write('ethernet service delete sid 1\n')
        bundlec.write('ethernet service add type p2p sid 1 admin operational evc-id ' + service_name + ' description ' + service_desc + '\n')
        #if oldal == 'belso':
        #    bundlec.write('platform sync source add eth-interface slot 1 port 1 priority 1 quality g.813/8262\n')
        #elif oldal == 'ugyfel':
        #    bundlec.write('platform sync source add radio-interface slot 2 port 1 radio-channel 0 priority 1 quality g.813/8262\n')
        bundlec.write('ethernet service sid 1\n')
        if mydatas[3] == 'tag':
            bundlec.write('sp add sp-type sap int-type bundle-c-tag spid 1 interface eth slot 1 port 1\n')
            bundlec.write('sp add sp-type sap int-type bundle-c-tag spid 2 interface radio slot 2 port 1\n')
            for i in range(0, len(vlan)):
                bundlec.write('sp bundle cvlan attach spid 1 vlan ' + vlan[i] + '\n')
                bundlec.write('sp bundle cvlan attach spid 2 vlan ' + vlan[i] + '\n')
        elif mydatas[3] == 'access':
            if oldal == 'ugyfel':
                bundlec.write('sp add sp-type sap int-type dot1q spid 1 interface eth slot 1 port 1 vlan untag\n')
            elif oldal == 'belso':
                bundlec.write('sp add sp-type sap int-type dot1q spid 1 interface eth slot 1 port 1 vlan ' + vlan[0] +'\n')
            bundlec.write('sp add sp-type sap int-type dot1q spid 2 interface radio slot 2 port 1 vlan ' + vlan[0] + '\n')
        bundlec.write('exit\n')
        bundlec.write('platform security access-control password edit own-password\n')




mydatas = (data_grabber(0))

if not os.path.exists('C:\\Temp\\' + mydatas[0]):             #ellenőrzi, hogy létezik e már a folder
    os.makedirs('C:\\Temp\\' + mydatas[0])                      #létrehoz egy foldert az uf_id nevével

write_common_lines(mydatas,'belso')
write_common_lines(mydatas,'ugyfel')
append_data(mydatas, 'belso')
append_data(mydatas, 'ugyfel')


