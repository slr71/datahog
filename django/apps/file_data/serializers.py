from rest_framework import serializers
from .models import *


class ImportedDirectorySerializer(serializers.ModelSerializer):
    date_scanned = serializers.DateTimeField(format=r'%Y-%m-%d %H:%M')
    class Meta:
        model = ImportedDirectory
        fields = ('id', 'date_scanned', 'folder_count', 'file_count', 'root_path', 
            'duplicate_count', 'total_size', 'size_timeline_data', 'type_chart_data', 'directory_type')


class FileSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format=r'%Y-%m-%d')
    #directory_type = serializers.CharField(source='directory.directory_type', read_only=True)
    class Meta:
        model = File
        fields = ('id', 'name', 'size', 'path', 'date_created', 'is_folder',)


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'name', 'total_size', 'path', 'is_folder')


class DupeGroupSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    class Meta:
        depth = 1
        model = DupeGroup
        fields = ('checksum', 'files', 'file_size', 'file_count', 'directories',)


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = ('id', 'extension', 'total_size')
