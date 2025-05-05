import shutil
from rest_framework import serializers
from .models import *
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


import shutil
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework import serializers
from .models import Folder, Files


class HandleFileUpload(APIView):

    class FileListSerializer(serializers.Serializer):
        files = serializers.ListField(
            child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False)
        )
        folder = serializers.CharField(required=False)
        password=  serializers.CharField(required=False)
        
        
        
        def zip_files(self, folder):

            source_folder = f'static/upload/{folder}'
            zip_path = f'static/zip/{folder}'

            if os.path.exists(source_folder):  # Check if folder exists
                shutil.make_archive(zip_path, 'zip', source_folder)
            else:
                raise ValueError(f"Source folder {source_folder} does not exist")

        def create(self, validated_data  ):
            password = validated_data.pop('password')

            folder = Folder.objects.create(password=password)
            files = validated_data.pop('files')

            files_objs = []

            for file in files:
                files_obj = Files.objects.create(folder=folder, file=file)
                files_objs.append(files_obj)

            try:
                print(folder.uid)
                self.zip_files(folder.uid)
            except ValueError as e:
                return {'status': 400, 'message': str(e)}

            return {
                'files': [
                    {
                        "id": file.id,
                        "file_url": file.file.url,  # Correctly reference the file URL
                        "uploaded_at": file.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
                    } for file in files_objs
                ],
                'folder': str(folder.uid)
            }


    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            serializer = self.FileListSerializer(data=request.data)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASDDDDDDDDDDDDDDDDD2")

            if serializer.is_valid():
                result = serializer.save()
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASDDDDDDDDDDDDDDDDD2")
                
                print(result)
                return Response({'status': 200, 'message': 'Files uploaded successfully', 'data': result})
            return Response({'status': 400, 'message': 'Something went wrong', 'data': serializer.errors})
        except Exception as e:
            return Response({'status': 500, 'message': f"Server error: {str(e)}"})
