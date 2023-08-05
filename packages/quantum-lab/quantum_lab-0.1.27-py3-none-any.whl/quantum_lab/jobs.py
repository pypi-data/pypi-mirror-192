import requests
import json
import time
import os

class quantum_lab():

    def __init__(self,
            resourceId: int,
            volumeName: str, 
            resourceName: str
        ):
        self.userID = os.environ["QCC_USER_ID"]
        # self.uploadType = uploadType
        # self.shot = shot
        self.resourceId = resourceId
        # self.filePath = filePath
        self.volumeName = volumeName
        self.resourceName = resourceName
        self.url = "http://job-management.qcc.svc.cluster.local"

    def error_handler(self, response):
        if response.status_code == 204:
            print(f"Status: {response.status_code}")
            print(f"ErrorMessage: Job not found.")
            return response.text
        print(f"Status: {response.status_code}")
        print(f"ErrorMessage: {response.json()['error']}")
        return {response.json()['error']}


    def createPrint(self,
            uploadType: str, 
            shot: int, 
            filePath: str, 
            timeout = 120
        ):
        url_path = f"{self.url}/qcc/notebook/job"

        headers = {
            "Content-Type": "application/json",
            "email": self.userID,
        }

        body = json.dumps({
            "uploadType": uploadType,
            "shot": shot,
            "resourceId": self.resourceId,
            "filePath": filePath,
            "volumeName": self.volumeName,
            "resourceName": self.resourceName
        })

        response = requests.post(f"{url_path}", headers=headers, data=body) 
        if response.status_code != 200:
            return self.error_handler(response)
        
        data = response.json()
        
        print("{:<6} {:<15}".format("ID", "Created Status"))
        print("{:<6} {:<15}".format(data["id"], 'Success' if data["status"] else 'Fail'))

        jobID = data["id"]

        time_num = 0
        while True:
            time.sleep(1)
            response = requests.get(f"{self.url}/qcc/notebook/job/{jobID}", headers=headers) 
            data = response.json()
            p_status = data["jobStatus"]
            print(f"Time: {time_num} / Job Status: {p_status}        ", end='\r')
            if p_status == "Success" or p_status == "Failed":
                break
            time_num += 1

            if time_num > timeout:
                print("TimeOut...")
                break

        
        return jobID

    def create(self, 
            uploadType: str, 
            shot: int, 
            filePath: str, 
        ):
        url_path = f"{self.url}/qcc/notebook/job"

        headers = {
            "Content-Type": "application/json",
            "email": self.userID,
        }

        body = json.dumps({
            "uploadType": uploadType,
            "shot": shot,
            "resourceId": self.resourceId,
            "filePath": filePath,
            "volumeName": self.volumeName,
            "resourceName": self.resourceName
        })

        response = requests.post(f"{url_path}", headers=headers, data=body) 
        if response.status_code != 200:
            return self.error_handler(response)
        
        data = response.json()
        

        print("{:<6} {:<15}".format("ID", "Created Status"))
        print("{:<6} {:<15}".format(data["id"], 'Success' if data["status"] else 'Fail'))
        
        return data["jobId"]

    def getList(self, limit = 0):
        url_path = f"{self.url}/qcc/notebook/jobs"

        headers = {
            "Content-Type": "application/json",
            "email": self.userID,
        }
        response = requests.get(f"{url_path}",headers=headers)
        
        if response.status_code != 200:
            return self.error_handler(response)
        
        data = response.json()

        print("{:<5} {:<10} {:<10} {:<12} {:<9} {:<8} {:<5} {:<11} {:<17} {:<30} {:<30}".format(
            "ID", 
            "JobID", 
            "ResourceID", 
            "ResourceName", 
            "RegStatus", 
            "Status", 
            "Shot",
            "UploadType",
            "FilePath", 
            "CreatedAt",
            "RunningAt"
            )
        )
        index = 0
        for ele in data["jobs"]:
            print("{:<5} {:<10} {:<10} {:<12} {:<9} {:<8} {:<5} {:<11} {:<17} {:<30} {:<30}".format(
                ele["id"], 
                ele["jobId"], 
                ele["resourceId"], 
                ele["resourceName"], 
                'True' if ele["jobRegStatus"] else 'False', 
                'NotReady' if ele["jobStatus"] is None else ele["jobStatus"],
                ele["jobShot"],
                ele["jobUploadType"],
                ele["jobFilePath"].split('/')[-1],
                ele["createdAt"],
                'NotReady' if ele["runningAt"] is None else ele["runningAt"]
                )
            )
            index += 1 
            if limit != 0 and index > limit:
                break

        return data["jobs"]

    def getJob(self, id: int):
        url_path = f"{self.url}/qcc/notebook/job/{id}"

        headers = {
            "Content-Type": "application/json",
            "email": self.userID,
        }
        response = requests.get(f"{url_path}", headers=headers)
        
        if response.status_code != 200:
            return self.error_handler(response)

        data = response.json()
        print("{:<5} {:<10} {:<10} {:<12} {:<9} {:<8} {:<5} {:<11} {:<17} {:<30} {:<30}".format(
            "ID", 
            "JobID", 
            "ResourceID", 
            "ResourceName", 
            "RegStatus", 
            "Status", 
            "Shot",
            "UploadType",
            "FilePath", 
            "CreatedAt",
            "RunningAt"
            )
        )
        print("{:<5} {:<10} {:<10} {:<12} {:<9} {:<8} {:<5} {:<11} {:<17} {:<30} {:<30}".format(
            data["id"], 
            data["jobId"], 
            data["resourceId"], 
            data["resourceName"], 
            'True' if data["jobRegStatus"] else 'False', 
            'NotReady' if data["jobStatus"] is None else data["jobStatus"],
            data["jobShot"],
            data["jobUploadType"],
            data["jobFilePath"].split('/')[-1],
            data["createdAt"],
            'NotReady' if data["runningAt"] is None else data["runningAt"]
            )
        )
        
        return data

    def delete(self, id: str):
        url_path = f"{self.url}/qcc/notebook/job/{id}"

        headers = {
            "Content-Type": "application/json",
            "email": self.userID,
        }
        response = requests.delete(f"{url_path}", headers=headers)

        if response.status_code != 200:
            return self.error_handler(response)

        print(f"Deleted job : {response.text}")

        return response.text
