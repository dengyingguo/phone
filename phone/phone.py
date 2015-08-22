#coding:utf-8

import os
import struct

__author__ = 'lovedboy'


class Phone(object):

    def __init__(self, dat_file=None):

        if dat_file is None:
            dat_file = os.path.join(os.path.dirname(__file__), "phone.dat")

        with open(dat_file, 'rb') as f:
            self.buf = f.read()

        self.head_fmt = "<4si"
        self.phone_fmt = "<iiB"
        self.head_fmt_length = struct.calcsize(self.head_fmt)
        self.phone_fmt_length = struct.calcsize(self.phone_fmt)
        self.version, self.first_phone_record_offset = struct.unpack(self.head_fmt, self.buf[:self.head_fmt_length])
        self.phone_record_count = (len(self.buf) - self.first_phone_record_offset) / self.phone_fmt_length

    def get_phone_dat_msg(self):
        print "版本号:{}".format(self.version)
        print "总记录条数:{}".format(self.phone_record_count)

    @staticmethod
    def get_phone_no_type(no):
        if no == 4:
             return "电信虚拟运营商"
        if no == 5:
            return  "联通虚拟运营商"
        if no == 6:
            return "移动虚拟运营商"
        if no == 3:
            return "电信"
        if no == 2:
            return "联通"
        if no == 1:
            return "移动"

    @staticmethod
    def _format_phone_content(phone, record_conent, phone_type):

        province, city, zip_code, area_code = record_conent.split('|')
        return {
            "phone": phone,
            "province": province,
            "city": city,
            "zip_code": zip_code,
            "area_code": area_code,
            "phone_type": Phone.get_phone_no_type(phone_type)
        }

    def _lookup_phone(self, phone):

        phone = str(phone)
        assert 7 <= len(phone) <= 11
        int_phone = int(str(phone)[0:7])

        left = 0
        right = self.phone_record_count
        while left <= right:
            middle = (left + right) / 2
            current_offset = self.first_phone_record_offset + middle * self.phone_fmt_length
            cur_phone, record_offset, phone_type = struct.unpack(self.phone_fmt,
                                                             self.buf[current_offset: current_offset + self.phone_fmt_length])

            if cur_phone > int_phone:
                right = middle - 1
            elif cur_phone < int_phone:
                left = middle + 1
            else:
                s = record_offset
                e = record_offset + self.buf[record_offset:].find('\0')
                record_content = self.buf[s: e]
                return Phone._format_phone_content(phone, record_content, phone_type)

    def find(self, phone):
        return self._lookup_phone(phone)

    @staticmethod
    def human_phone_info(phone_info):

        if not phone_info:
            return ''

        return "{}|{}|{}|{}|{}|{}".format(phone_info['phone'],phone_info['province'], phone_info['city'],
                                    phone_info['zip_code'], phone_info['area_code'],phone_info['phone_type'])

    def test(self):
        self.get_phone_dat_msg()

        for i in xrange(1529900, 1529999):
            print self.human_phone_info(self.find(i))

if __name__ == "__main__":

    phone = Phone()
    phone.test()


