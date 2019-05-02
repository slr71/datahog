import irods
import requests
import json
import os
import pickle
from subprocess import call
from rest_framework.response import Response
from rest_framework import views

from .models import *
from .serializers import *
from .tasks import *
from apps.file_data.models import ImportedDirectory


class GetImportContext(views.APIView):
    def get(self, request):
        try:
            last_attempt = ImportAttempt.objects.latest('date_imported')
        except ImportAttempt.DoesNotExist:
            last_attempt = ImportAttempt()

            iplant_user = os.environ.get('IPLANT_USER')
            if iplant_user:
                last_attempt.irods_user   = iplant_user
                last_attempt.cyverse_user = iplant_user
                last_attempt.irods_root   = '/iplant/home/{}'.format(iplant_user)
                last_attempt.cyverse_root = '/iplant/home/{}'.format(iplant_user)
            
            last_attempt.save()
        
        serializer = ImportAttemptSerializer(last_attempt)
        num_sources = ImportedDirectory.objects.count()
        
        return Response({
            'last_attempt': serializer.data,
            'num_sources': num_sources
        })


class GetLastTask(views.APIView):
    def get(self, request):
        try:
            last_task = AsyncTask.objects.latest('timestamp')
        except AsyncTask.DoesNotExist:
            last_task = AsyncTask.objects.create()
        
        serializer = AsyncTaskSerializer(last_task)
        return Response(serializer.data)


class DeleteDirectory(views.APIView):
    def delete(self, request):
        try:
            source = ImportedDirectory.objects.get(id=request.data['source'])
        except:
            return Response('Source not found.', status=400)

        new_task = AsyncTask.objects.create(
            in_progress=True,
            status_message='Deleting source...'
        )
        
        delete_source.delay(new_task.id, source_id=source.id)
        serializer = AsyncTaskSerializer(new_task)
        return Response(serializer.data)


class ImportFromIrods(views.APIView):
    def post(self, request):
        required_fields = ('user', 'password', 'host', 'port', 'zone', 'root', 'name')
        for field in required_fields:
            if field not in request.data:
                return Response('Missing required field: {}'.format(field), status=400)

        user = request.data['user']
        password = request.data['password']
        host = request.data['host']
        port = request.data['port']
        zone = request.data['zone']
        root = request.data['root']
        name = request.data['name']
        
        with irods.session.iRODSSession(
            user=user,
            password=password,
            host=host,
            port=port,
            zone=zone,
        ) as session:
            try:
                session.collections.get(root)
            except irods.exception.NetworkException:
                return Response('Unable to connect to iRODS server at {}:{}.'.format(host, port), status=400)
            except irods.exception.CAT_INVALID_AUTHENTICATION:
                return Response('Invalid authentication credentials.', status=400)
            except irods.exception.CollectionDoesNotExist:
                return Response('The requested folder does not exist.', status=400)
            except Exception as e:
                return Response('Error: {}'.format(e))
        
        
        last_attempt = ImportAttempt.objects.latest('date_imported')

        new_attempt = ImportAttempt.objects.create(
            irods_user=user,
            irods_host=host,
            irods_port=port,
            irods_zone=zone,
            irods_root=root,
            irods_name=name,

            cyverse_user=last_attempt.cyverse_user,
            cyverse_root=last_attempt.cyverse_root,
            cyverse_name=last_attempt.cyverse_name,
            
            s3_key=last_attempt.s3_key,
            s3_bucket=last_attempt.s3_bucket,
            s3_root=last_attempt.s3_root,
            s3_name=last_attempt.s3_name,
        )

        new_task = AsyncTask.objects.create(
            in_progress=True,
            status_message='Starting import process...',
            status_subtitle='This may take several minutes.',
            import_attempt=new_attempt
        )

        import_files_from_irods.delay(new_task.id, password=password)

        serializer = AsyncTaskSerializer(new_task)
        return Response(serializer.data, status=200)


class ImportFromCyverse(views.APIView):
    def post(self, request):
        required_fields = ('user', 'password', 'root', 'name')
        for field in required_fields:
            if field not in request.data:
                return Response('Missing required field: {}'.format(field), status=400)

        user = request.data['user']
        password = request.data['password']
        root = request.data['root']
        name = request.data['name']
        
        try:
            response = requests.get(
                'https://de.cyverse.org/terrain/token',
                auth=(user, password)
            )
        except Exception as e:
            return Response('Unable to connect to the CyVerse.', status=500)

        auth_info = json.loads(response.text)
        if 'access_token' not in auth_info:
            return Response('Invalid authentication credentials.', status=400)

        auth_token = 'Bearer {}'.format(auth_info['access_token'])
        
        last_attempt = ImportAttempt.objects.latest('date_imported')

        new_attempt = ImportAttempt.objects.create(
            irods_user=last_attempt.irods_user,
            irods_host=last_attempt.irods_host,
            irods_port=last_attempt.irods_port,
            irods_zone=last_attempt.irods_zone,
            irods_root=last_attempt.irods_root,
            irods_name=last_attempt.irods_name,

            cyverse_user=user,
            cyverse_root=root,
            cyverse_name=name,
            
            s3_key=last_attempt.s3_key,
            s3_bucket=last_attempt.s3_bucket,
            s3_root=last_attempt.s3_root,
            s3_name=last_attempt.s3_name,
        )

        new_task = AsyncTask.objects.create(
            in_progress=True,
            status_message='Starting import process...',
            status_subtitle='This may take several minutes.',
            import_attempt=new_attempt
        )

        import_files_from_cyverse.delay(new_attempt.id, auth_token=auth_token)

        serializer = AsyncTaskSerializer(new_task)
        return Response(serializer.data, status=200)


class ImportFromFile(views.APIView):
    def post(self, request):
        if 'name' not in request.data:
            return Response('Missing required field: name', status=400)
        if 'file' not in request.FILES:
            return Response('File not found.', status=400)

        name = request.data['name']
        file = request.FILES['file']

        try:
            file_data = pickle.load(file)
            assert file_data['format'] in ('datahog:0.1',)
        except:
            return Response('Not a valid .datahog file.', status=400)

        last_attempt = ImportAttempt.objects.latest('date_imported')

        new_attempt = ImportAttempt.objects.create(
            file_name=name,

            irods_user=last_attempt.irods_user,
            irods_host=last_attempt.irods_host,
            irods_port=last_attempt.irods_port,
            irods_zone=last_attempt.irods_zone,
            irods_root=last_attempt.irods_root,
            irods_name=last_attempt.irods_name,

            cyverse_user=last_attempt.cyverse_user,
            cyverse_root=last_attempt.cyverse_root,
            cyverse_name=last_attempt.cyverse_name,
            
            s3_key=last_attempt.s3_key,
            s3_bucket=last_attempt.s3_bucket,
            s3_root=last_attempt.s3_root,
            s3_name=last_attempt.s3_name,
        )

        new_task = AsyncTask.objects.create(
            in_progress=True,
            status_message='Starting import process...',
            status_subtitle='This may take several minutes.',
            import_attempt=new_attempt
        )

        import_files_from_file.delay(new_task.id, file_data)

        serializer = AsyncTaskSerializer(new_task)
        return Response(serializer.data, status=200)


class ImportFromS3(views.APIView):
    def post(self, request):
        required_fields = ('key', 'secret', 'bucket', 'name')
        for field in required_fields:
            if field not in request.data:
                return Response('Missing required field: {}'.format(field), status=400)

        key = request.data['key']
        secret = request.data['secret']
        bucket = request.data['bucket']
        name = request.data['name']
        root = request.data['root']
    
        client = boto3.client('s3',
            aws_access_key_id=key,
            aws_secret_access_key=secret
        )

        try:
            client.list_buckets()
        except:
            return Response('Invalid AWS credentials.')
        
        try:
            client.head_bucket(Bucket=bucket)
        except:
            return Response('Unable to access the requested bucket.')

        if len(root):
            try:
                client.head_object(Bucket=bucket, Key=root)
            except:
                return Response('Unable to find the requested folder.')

        last_attempt = ImportAttempt.objects.latest('date_imported')
        new_attempt = ImportAttempt.objects.create(
            irods_user=last_attempt.irods_user,
            irods_host=last_attempt.irods_host,
            irods_port=last_attempt.irods_port,
            irods_zone=last_attempt.irods_zone,
            irods_root=last_attempt.irods_root,
            irods_name=last_attempt.irods_name,

            cyverse_user=last_attempt.cyverse_user,
            cyverse_root=last_attempt.cyverse_root,
            cyverse_name=last_attempt.cyverse_name,
            
            s3_key=key,
            s3_bucket=bucket,
            s3_root=root,
            s3_name=name,
        )

        import_files_from_s3.delay(new_attempt.id, secret_key=secret)

        serializer = ImportAttemptSerializer(new_attempt)
        return Response(serializer.data, status=200)
