import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def google_drive_auth():
    global drive


class Upload:
    # chandan_zips_reasoning = '1XnppfJ1G4a8RbSZF9HALUEJD38x2hSEu'
    chandan_zips_arithematics = '1cpw61nGRn_TfOHa2FtrOy9h0z3ZBVP7L'




    def __init__(self,call_back):

        self.call_back = call_back

        self.folder_id = self.chandan_zips_arithematics
        self.team_drive_id = '0AA-mJZpOW19XUk9PVA'

        self.auth()



    def auth(self):
        gauth = GoogleAuth()

        # Try to load saved client credentials
        try:
            gauth.LoadCredentialsFile("mycreds.txt")
        except:
            pass

        if gauth.credentials is None:
            # Authenticate if they're not there

            # This is what solved the issues:
            gauth.GetFlow()
            gauth.flow.params.update({'access_type': 'offline'})
            gauth.flow.params.update({'approval_prompt': 'force'})

            gauth.LocalWebserverAuth()

        elif gauth.access_token_expired:

            # Refresh them if expired
            gauth.Refresh()
        else:

            # Initialize the saved creds

            gauth.Authorize()

        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")

        self.drive = GoogleDrive(gauth)

    def set_zip_location(self,zip_location):

        self.zip_location = zip_location
        self.zip_name = os.path.basename(self.zip_location)[:-4]






    def upload(self):

        f = self.drive.CreateFile({
            'title': self.zip_name,
            'mimetype': 'zip',
            'parents': [{
                'kind': 'drive#fileLink',
                'teamDriveId': self.team_drive_id,
                'id': self.folder_id
            }]
        })
        f.SetContentFile(self.zip_location)

        try:
            f.Upload(param={'supportsTeamDrives': True})
            self.call_back("Uploading to drive of "+ str(self.zip_name) + "Succeed")
        except Exception as e:
            print(e)
            self.call_back("Exception happened"+str(e))





