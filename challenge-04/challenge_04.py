import csv
import sys
import argparse
import os
import socket
import requests
from datetime import datetime
import concurrent.futures
import threading
import time


class FQDN:

    def __init__(self, option=None):
        if option:
            self.fqdn_file = open(option.input_file, 'r')
            reader = csv.reader(self.fqdn_file)
            next(reader, None) # skip the headers
            output_csv = open(option.output_file, 'w')
            self.csv_writer_lock = threading.Lock()
            self.writer = csv.writer(output_csv)
            self.writer.writerow(['FQDN', 'IP', 'DNS_time_ms', 'HTTP_handshake_time_ms'])

            t1 = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor(option.thread_count) as executor:
                executor.map(self.process_and_write_output, reader)
            
            # ******************************************
            # Leaving this single thread code to demonstrate the reduced timetaken by multi processing
            # ********************************************
            # for i in reader:
            #     self.process_and_write_output(i)

            t2 = time.perf_counter()
            print(f"Total processing took {t2-t1} seconds......")
            
            self.fqdn_file.close()


    def process_and_write_output(self, item):
        print(item)
        host = item[0].strip()
        print("Host", host)
        ip, et = self.get_ip_for_host(host)
        if ip:
            hs_et = self.handshake_ip(ip)
        else:
            hs_et = 'NA'
        self.write_to_output([host, ip, "{:.2f}".format(et), "{:.2f}".format(hs_et)])
        # self.writer.writerow([host, ip, et, hs_et])



    def write_to_output(self, row):
        with self.csv_writer_lock:
            self.writer.writerow(row)
        


    def get_ip_for_host(self, host):
        start = datetime.now()
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            ip = ''
        return ip, (datetime.now()-start).total_seconds() * 1000


    def handshake_ip(self, ip):
        start = datetime.now()
        try:
            a = requests.get('http://{}'.format(ip), timeout=3)
        except:
            pass
        
        return (datetime.now()-start).total_seconds() * 1000

def get_args():

    def validate_csv(parser, file):
        if not os.path.exists(file):
            parser.error("Given file {} does not exists..".format(file))

        elif not file.endswith('.csv'):
            parser.error("Please provide a valid {} file".format(ext))

        return file

    def validate_path(parser, file):
        path, filename = os.path.split(file)
        if path and not os.path.exists(path):
            parser.error("Invalid Output Path..")

        if not filename.endswith('.csv'):
            parser.error("Output file should be a CSV file..")

        return file


    parser = argparse.ArgumentParser(description="Update IP & time taken for HTTP handshake for the given FQDN")
    parser.add_argument('--input', dest='input_file', type=lambda f: validate_csv(parser, f), required=True)
    parser.add_argument('--thread-count', dest='thread_count', type=int, default=1)
    parser.add_argument('--output', dest='output_file', type=lambda f: validate_path(parser, f), default='output.csv')

    return parser.parse_args()





if __name__ == '__main__':

    args = get_args()
    FQDN(option = args)
    
