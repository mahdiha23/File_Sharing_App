from django.db import models
import uuid
import os



 
def get_upload_path(instance, filename):
    folder_name = str(instance.folder.uid)
    return os.path.join("upload", folder_name, filename)  # Explicit full path


class Folder(models.Model):
    uid=models.UUIDField(primary_key =True , editable=False , default=uuid.uuid4)
    created_at=models.DateField(auto_now=True)
    password=models.CharField( max_length=50 , null=False)
  
  
    def __str__(self):
        return f"{self.uid} --  {self.created_at}"
    
    
class Files(models.Model):
    folder=models.ForeignKey(Folder , on_delete=models.CASCADE)    
    file = models.FileField(upload_to=get_upload_path)
    created_at=models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.file} --  {self.created_at}"