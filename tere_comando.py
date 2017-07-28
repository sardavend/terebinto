import httplib
import urllib
import argparse

from config import SIM_NUMBERS, SMS_SERVICES_IP, SMS_SERVICES_PORT



def get_sim_numbers():
	if len(SIM_NUMBERS) >= 8:
		return SIM_NUMBERS.replace(" ","").split(",")


def send_sms(recipients, message):
	print recipients
	conn = httplib.HTTPConnection(SMS_SERVICES_IP, SMS_SERVICES_PORT)
	recipients = ["591" + recipt for recipt in recipients]
	to = " ".join(recipients)
	text = "&text=" + urllib.quote(message)
	url = "/cgi-bin/sendsms?username=usr&password=pass&to=" + urllib.quote(to) + text
	print url
	conn.request("GET", url)
	response = conn.getresponse()
	print response.status
	if response.status == 202:
		print "telecomando {0} enviado correctamente a {1}".format(message, recipients)
	conn.close()

def get_num_of_batchs(number_list_len):
	#Sent a command every 10 numbers at time
	return (number_list_len - 1) / 10

def get_list_indexes(batchs):
	list_of_indexes = []
	for n in range(batchs + 1):
		s = n * 10
		if n == batchs:
			list_of_indexes.append([s, -1])
		else:
			list_of_indexes.append([s, s + 9])
	return list_of_indexes



def main(command):
	sim_num = get_sim_numbers()
	if not sim_num:
		print "Introduce at least one valid sim number"
		return 
	sim_num_len = len(sim_num)
	if sim_num_len > 0:
		batchs = get_num_of_batchs(sim_num_len)
		indexes_range = get_list_indexes(batchs)
		for index, r in enumerate(indexes_range):
			if index == (len(indexes_range) - 1):
				send_sms(sim_num[r[0]::], command)
				return 
			send_sms(sim_num[r[0]:r[1] + 1], command)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("command", type=str, help="command to send")
	args = parser.parse_args()
	if args.command is None:
		print "You need to specify a command to send to"
	else:
		main(args.command)






