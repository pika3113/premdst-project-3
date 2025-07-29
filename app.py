import csv
from flask import Flask, render_template,request,jsonify

def timeconv(secs):
  return divmod(secs,60)

def run(pt,age):
  #830-1820 convert to seconds
  data=list(csv.reader(open('run.csv', newline='')))
  pt = timeconv(pt)
  pts = max(0, min(((int(pt[0]) * 60+int(pt[1]))-510)//10, 59))
  return int(data[pts][age]) if data[pts][age] != '' else 50

def situp(pt,age):
  #60-1
  pt = max(0, min(pt-1, 59))
  data=list(csv.reader(open('situp.csv', newline='')))
  return int(data[pt][age]) if data[pt][age] != '' else 25

def pushup(pt,age):
  #60-1
  pt = max(0,min(pt-1,59))
  data=list(csv.reader(open('pushup.csv', newline='')))
  return int(data[pt][age]) if data[pt][age] != '' else 25

def deterage(age):
  a=max(0,min(((int(age)-19)//3),13))
  #print(a)
  return int(a)

app = Flask(__name__)

@app.route('/')
def home(name=''):
  return render_template('ippt.html',name=name)

@app.route('/calculate',methods=['POST'])
def calculate():
  data=request.get_json()
  print(data)
  age = int(data.get('age',0))
  pushups = int(data.get('pushup',0))
  situps = int(data.get('situp',0))
  runtime = int(data.get('run',7200))
  age = deterage(age)
  
  print(age,pushups,situps,runtime)

  score=0
  score+=pushup(pushups,age)+situp(situps,age)+run(runtime,age)
  if score>89:
      type='gold (commandos)'
      color='#f2b90f'
  elif score>84:
    type='gold'
    color='#ffce3b'
  elif score>74:
    type='silver'
    color='#999999'
  elif score>60:
    type='pass (with incentive)'
    color='#00ff1a'
  elif score>50:
    type='pass'
    color='#ff9900'
  else:
    type='fail'
    color='#fc1e31'

  ret = str(round(score))+' '+type

  return jsonify({
	  'score':ret,
    'color':color
  })



def ippt():
  ippt = [60,60,'20:30']
  age = ''

  while not age.isdigit():
    age = input('Age: ')
  age = deterage(int(age))

  print(pushup(ippt[0],age))
  print(situp(ippt[1],age))
  print(run(ippt[2],age))
  result = situp(ippt[0],age)+pushup(ippt[1],age)+run(ippt[2],age)
  print(result)


#ippt()
if __name__ == '__main__':
  app.run(debug=True)

