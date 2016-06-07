#!/usr/bin/python
#coding:utf-8
#by cvv54
 
import sys
import os
import re
 
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
 
try:
    tree = ET.parse("/home/test/case/usecase.xml")
    #root = ET.fromstring(country_string)
    root = tree.getroot()
except Exception,e:
    print "Error:cannot parse file:usecase.xml."
    sys.exit(1)
print root.tag,"---",root.attrib
for child in root:
    print child.tag,"---",child.attrib
 
passed=0
failed=0    
 
for case in root.findall('case'):
    pre = case.find('pre').text
    perform = case.find('perform').text
    expect = case.find('expect').text.strip('\n')
    id = case.get("id")
 
    print "key words are :"    
    print expect
 
    for each in pre.split(';'):
#        print each
        if not each.strip()=='':
            command = each.strip('\n')
            os.environ['command']=str(command)
            print command
         
            os.system("kdestroy")
            os.system("kinit -kt /etc/security/keytabs/single.keytab single")
            os.system('beeline -u "jdbc:hive2://gateway.xxx.xxx:10000/;principal=single" -e "$command;" &>>log')
 
    for each in perform.split(';'):
#        print each
        if not each.strip()=='':
            command = each.strip('\n')
            os.environ['command']=str(command)
            print command
         
            os.system("kdestroy")
            os.system("kinit -kt /etc/security/keytabs/test.keytab test")
            os.system('beeline -u "jdbc:hive2://gateway.xxx.xxx:10000/;principal=single" -e "$command;" &>tmp')
    
    f=open('tmp')
    flag=0
    for line in f:
#        print "line is :"
#        print line
        match=re.findall(expect,line)
        if match != []:
            passed+=1
            flag=1
         
    if flag == 0:
        failed+=1            
        print(id)
     
    os.system("cat tmp>>log")
    os.system("rm -f tmp")
 
print "passed:"
print passed
print "failed:"
print failed
 
os.system('mv log `date "+%Y-%m-%d~%H-%M-%S"`')
