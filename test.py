__author__ = 'JennaKwon'


with open("companies", 'r') as f:
    for line in f:
        company = line.rstrip().partition(' ')[0]
        print(company)

