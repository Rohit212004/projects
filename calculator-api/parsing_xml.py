import xml.etree.ElementTree as ET
tree = ET.parse('Rohit.xml')
root = tree.getroot()

print("Root element:", root.tag)

for student in root.findall('student'):
    name = student.find('name').text
    age = student.find('age').text
    branch= student.find('branch').text
    year= student.find('year').text
    cgpa= student.find('cgpa').text
    rollno= student.find('rollno').text
    print(f" Name: {name}\n Age: {age}\n branch: {branch}\n Year: {year}\n CGPA: {cgpa}\n Roll No: {rollno}")