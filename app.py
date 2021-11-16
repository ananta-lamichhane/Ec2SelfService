from flask import Flask, render_template, request, jsonify, url_for, redirect
import boto3

from botocore.exceptions import ClientError
import json

app = Flask(__name__)


'''
    boto3 takes profile name from the ~/.aws/credentials file
    we can switch these
    aws command line can be used to create session token
'''
session = boto3.Session(profile_name='fsx_ad')
#aws_session.resource(service_name='ec2')
ec2client = session.client('ec2', region_name="eu-west-1")

'''
called by the web app, takes instance id and action (str:"start"|"stop") as param.
'''
def start_stop_instance(instance_id, action):
    if action == "start":
        try:
            ec2client.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        try:
            response = ec2client.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
    elif action == "stop":
        try:
            ec2client.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        try:
            response = ec2client.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)



@app.route('/', methods=['GET', 'POST'])
def home():
    instances = []
    try:
        all_res = ec2client.describe_instances()['Reservations']
        for i in range(0,len(all_res)):
            res = all_res[i]
            print(res['Instances'][0])
            instances.append(res['Instances'][0])
    except ClientError as e:
        print(f'Error {e}')
    print("test")
    #print(instances)
    if request.method == "POST":
        instance_name = request.form.get("instance_name")
        instance_type = request.form.get("instance_type")
        key_pair = request.form.get("key_pair")

        response = ec2client.run_instances(
            SubnetId = "subnet-00b582984cc42fc5f",# "subnet-07b3ed7c49e80e40f" #(ananta-test-controltower private 2),
            ImageId= "ami-08edbb0e85d6a0a07",
            MinCount= 1,
            MaxCount = 1,
            InstanceType='t2.micro',## need to extend this functinality later.
            KeyName='windows_test_ec2'

        )

       # print(response)
    return render_template("index.html" ,instances=instances)


@app.route('/changeStatus')
def changeStatus():
    instance_id = request.args.get('instance_id')
    action = request.args.get('action')
    print("please start this instance" + instance_id)
    start_stop_instance(instance_id, action)
    instances = ec2client.describe_instances()['Reservations'][0]['Instances']
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()

