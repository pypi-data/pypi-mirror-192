from requests import get, post

class SquareCloud:
    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": token}

    def get_applications(self):
        user_links = "https://api.squarecloud.app/v1/public/user"
        request = get(user_links, headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        applications = response["response"]["applications"]
        return applications

    def get_application_by_id(self, application_id: str):
        applications = self.get_applications()
        for application in applications:
            if application["id"] == application_id:
                return application

    def backup_application(self, application_id: str):
        link_backup = f"https://api.squarecloud.app/v1/public/backup/{application_id}"
        request = get(link_backup, headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        backup_url = response["response"]['downloadURL']
        return backup_url
    
    def get_status_application(self, application_id: str):
        status_url = f"https://api.squarecloud.app/v1/public/status/{application_id}"
        request = get(status_url,headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        return response["response"]
    
    def is_running(self, application_id: str):
        application_status = self.get_status_application(application_id)
        if not application_status:
            return
        return application_status["running"]

    def get_most_recents_logs(self,application_id:str):
        logs_url = f"https://api.squarecloud.app/v1/public/logs/{application_id}"
        request = get(logs_url,headers = self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        logs = response["response"]["logs"]
        return logs

    def get_full_terminal_link(self,application_id: str):
        full_terminal_url = f"https://api.squarecloud.app/v1/public/full-logs/{application_id}"
        request = get(full_terminal_url,headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        logs_url = response["response"]["logs"]
        return logs_url

    def start_application(self, application_id: str):
        start_url = f"https://api.squarecloud.app/v1/public/start/{application_id}"
        request = post(start_url,headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        return True

    def stop_application(self, application_id: str):
        stop_url = f"https://api.squarecloud.app/v1/public/stop/{application_id}"
        request = post(stop_url,headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        return True

    def restart_application(self,application_id: str):
        restart_url = f"https://api.squarecloud.app/v1/public/restart/{application_id}"
        request = post(restart_url,headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        return True

    def delete_application(self,application_id: str):
        delete_url = f"https://api.squarecloud.app/v1/public/delete/{application_id}"
        request = post(delete_url,headers=self.headers)
        response = request.json()
        if response["status"] != "success":
            return
        return True
