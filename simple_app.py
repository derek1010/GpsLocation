from pynmea.streamer import NMEAStream


# {'GPRMC', 'GPGGA', 'GPGSV','GPVTG'}


def parseAveragePRN(nmea_objects):
    result = {}
    sen_type = {}
    ttff = False

    for nmea_ob in nmea_objects:
        if nmea_ob.sen_type == "GPRMC" and not ttff:
            if nmea_ob.timestamp:
                ttff = True;
                print nmea_ob.nmea_sentence
                continue 
        if ttff:
            if nmea_ob.sen_type == "GPGSV" or nmea_ob.sen_type == "GLGSV":
                if nmea_ob.msg_num < nmea_ob.num_messages:
                    for j in range(1,5):
                        if eval("nmea_ob.sv_prn_num_%d"%(j,)) not in result:
                            if eval("nmea_ob.snr_%d"%(j,)):
                                result[eval("nmea_ob.sv_prn_num_%d"%(j,))] = [eval(eval("nmea_ob.snr_%d"%(j,))), 1]
                        else:
                            if eval("nmea_ob.snr_%d"%(j,)):
                                result[eval("nmea_ob.sv_prn_num_%d"%(j,))] = [result[eval("nmea_ob.sv_prn_num_%d"%(j,))][0] + \
                                                                    eval(eval("nmea_ob.snr_%d"%(j,))), \
                                                                                  result[eval("nmea_ob.sv_prn_num_%d"%(j,))][1] + 1]
                else:
                    if nmea_ob.num_sv_in_view:
                        if nmea_ob.num_sv_in_view.startswith("0"):
                            nmea_ob.num_sv_in_view = nmea_ob.num_sv_in_view[1]
                        i = eval(nmea_ob.num_sv_in_view) % 4
                        for k in range(1,i+1):
                            if eval("nmea_ob.sv_prn_num_%d"%(k,)) not in result:
                                if eval("nmea_ob.snr_%d"%(k,)):
                                    result[eval("nmea_ob.sv_prn_num_%d"%(k,))] = [eval(eval("nmea_ob.snr_%d"%(k,))), 1]
                            else:
                                if eval("nmea_ob.snr_%d"%(k,)):
                                    result[eval("nmea_ob.sv_prn_num_%d"%(k,))] = [result[eval("nmea_ob.sv_prn_num_%d"%(k,))][0] + \
                                                                    eval(eval("nmea_ob.snr_%d"%(k,))), \
                                                                                  result[eval("nmea_ob.sv_prn_num_%d"%(k,))][1] + 1]
                   
    del result[""]
    print result
    for key in result:
        result[key][0] = result[key][0]/result[key][1]
        print [ key,result[key][0]]


def parseAverageLocation(nmea_objects):
    result = {}
    for nmea_ob in nmea_objects:
        if nmea_ob.sen_type == "GPRMC":
            if nmea_ob.timestamp:
                if "location" in result:
                    result["location"] = [result["location"][0] + \
                                          eval(nmea_ob.lat), result["location"][1] + eval(nmea_ob.lon), result["location"][2] + 1]
                else:
                    result["location"] = [eval(nmea_ob.lat), eval(nmea_ob.lon), 1]
    #print 'total lat and lon are :', result
    #print 'average lat and lon are :', result["location"][0]/result["location"][2] , result["location"][1]/result["location"][2]
    temp = "%f"%(result["location"][0]/result["location"][2],)
    temp2 = "%f"%(result["location"][1]/result["location"][2],)
    print "average lat and lon of %d locations are: "%result["location"][2],eval(temp[2:])/60 + eval(temp[0:2]),"  ", eval(temp2[3:])/60 + eval(temp2[0:3])
    '''3112.07228075 12135.9631889'''
    '''3112.06838862 12135.9582695'''
    '''31.2011449167  121.599330883'''



if __name__ == "__main__":

    #data_file = '../tests/test_data/test_data.gps'
    #data_file = './log_0519/HTC_GPS_NMEA_16.49.44.txt'
    #data_file = './log_0519/2/HTC_GPS_NMEA_17.51.54.txt'
    #data_file = '/home/derek/Desktop/qctlog/0527/HTC_GPS_NMEA_14.39.44.txt'
    data_file = './log0529/HTC_GPS_NMEA_17.14.02.txt'
    with open(data_file, 'r') as data_file_fd:
        nmea_stream = NMEAStream(stream_obj=data_file_fd)
        next_data = nmea_stream.get_objects()
        nmea_objects = []
        while next_data:
            nmea_objects += next_data
            next_data = nmea_stream.get_objects()

    # All nmea objects are now in variable nmea_objects
        parseAveragePRN(nmea_objects)
        parseAverageLocation(nmea_objects)






